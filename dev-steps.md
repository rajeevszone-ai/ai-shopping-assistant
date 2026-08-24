## This document contains info on what all analysis was done to develop the ai-shopping-assistant

### Datasets
[Meta Categories](https://huggingface.co/datasets/McAuley-Lab/Amazon-Reviews-2023/blob/main/raw/meta_categories/meta_Sports_and_Outdoors.jsonl)
[Review Categories](https://huggingface.co/datasets/McAuley-Lab/Amazon-Reviews-2023/blob/main/raw/review_categories/Sports_and_Outdoors.jsonl)



### Dataset Architecture Comparison

| Metric / Feature | [Flipkart Fashion](https://www.kaggle.com/datasets/aaditshukla/flipkart-fasion-products-dataset) | [E-Commerce Products](https://www.kaggle.com/datasets/mewbius/ecommerce-products) | [Amazon Reviews 2023: Sports & Outdoors](https://huggingface.co/datasets/McAuley-Lab/Amazon-Reviews-2023/tree/main) |
| :--- | :--- | :--- | :--- |
| **Domain Fit for REI** | **Poor** (Focused strictly on general fashion, traditional Indian apparel, and lifestyle wear). | **Excellent** (Scraped directly from **L.L. Bean**, a primary outdoor competitor to REI). | **Excellent** (Comprehensive coverage of camping, hiking, climbing, skiing, and water sports). |
| **Data Source Files** | Single CSV (`flipkart_fashion_products_dataset.csv`). | Catalog CSVs (`productsfull2.csv`) + Taxonomy mappings. | `meta_Sports_and_Outdoors.jsonl` (specs) + `review_Sports_and_Outdoors.jsonl` (Q&A feedback). |
| **Technical Spec Depth** | **Low** (Basic clothing attributes: color, size, fabric, gender). | **Medium-High** (Outdoor clothing/gear specs, temperature ratings, materials). | **Very High** (Bulleted technical specs, dimensions, weight in oz/lbs, insulation, materials). |
| **Rufus Use Case Alignment** | Basic keyword shopping (*"red t-shirt"*). | Outdoor product discovery & category navigation. | **Exact Rufus match** (Answers technical queries, performance questions, & multi-condition gear advice). |

### Vector Database Architecture & Cost Comparison

| Metric / Feature | [ChromaDB](https://www.trychroma.com/) | [FAISS (Meta)](https://github.com/facebookresearch/faiss) | [Qdrant](https://qdrant.tech/) |
| :--- | :--- | :--- | :--- |
| **Recommendation Status** | **Top Pick (Phase 1 / Prototype)** | **Not Recommended** | **Top Pick (Phase 2 / Production)** |
| **Recommendation Rationale** | Zero setup required; native dictionary-based metadata filtering matches your price/category constraints perfectly for local Python dev. | Lacks native metadata filtering capabilities, making complex e-commerce queries (e.g., price <= $100) difficult and inefficient to implement. | Enterprise-ready vector database with powerful payload filtering and a generous free cloud tier, ideal for scaling beyond a local file store. |
| **Best For** | Rapid Python prototyping, local dev, & embedded apps. | In-memory vector arithmetic & low-latency C++ tasks. | High-scale, cloud-native vector search & production RAG. |
| **Metadata Pre-Filtering** | **Native & Simple** (Python dict syntax: `price`, `category`). | **Manual / Complex** (Requires custom ID indexing wrappers). | **Native & High-Performance** (Payload filtering). |
| **Persistence Model** | Zero-config SQLite file (`./data/chroma_db`). | Manual export/import to disk (`.index` binary files). | Embedded mode or Docker / Managed Cloud instance. |
| **MCP Integration** | `@modelcontextprotocol/server-sqlite` | None (Requires writing a custom server wrapper). | `@qdrant/mcp-server` |
| **Local Cost (Dev)** | **$0 / month** (Runs in-process using local disk space). | **$0 / month** (Runs entirely in system RAM). | **$0 / month** (Runs via Docker or embedded Python client). |
| **Cloud Cost (Production)**| **$0 software cost** (Self-host via EC2/Docker container). | **$0 software cost** (Self-host compute instance required). | **$0 - $130+/mo** ($0 free tier; $30-$130/mo managed cloud; $30-$96/mo VPS self-hosted). |


### Why You Should NOT Join Product & Review Categories into One DataFrame

1. **Massive Data Explosion (1-to-Many Mismatch)**
   * **`raw_meta` (Product Catalog)**: ~1.6 million items.
   * **`raw_review` (User Feedback)**: ~16.8 million user reviews.
   * Merging these datasets on `parent_asin` via Pandas duplicates the product's title, price, store, and spec features **for every single review record**.
   * A 10 GB raw JSONL file will expand into a **50–80 GB merged dataset**, leading to out-of-memory (OOM) system crashes on standard local hardware.

2. **Diluted Retrieval Quality**
   * Combining individual, highly specific user reviews directly with core product metadata pollutes the semantic vector space.
   * Negative or edge-case review comments (e.g., *"The zipper broke on my second trip"*) can distort the product's primary vector representation, causing irrelevant or low-quality search results when querying for standard specs (e.g., *"lightweight 2-person tents"*).

3. **Database Inefficiency & Redundancy**
   * Storing identical product spec text repeatedly across millions of vector rows wastes disk storage, increases indexing costs, and slows down nearest-neighbor search queries.
   * Vector search works best when keeping entities distinct: querying **Products** for feature search and querying **Reviews** as an isolated lookup layer for social proof and user feedback.

---

### Recommended 2-Phase Data Strategy

Instead of joining datasets into a single frame, implement a decoupled two-phase retrieval pattern:

```text
USER QUERY
                          │
                          ▼
        ┌───────────────────────────────────┐
        │  Phase 1: Product Catalog Vector  │ ◄── (ChromaDB Collection: 'rei_products')
        │  Search (Filtering + Semantics)   │     Metadata: price, category, store, rating
        └─────────────────┬─────────────────┘
                          │
                          ▼
        ┌───────────────────────────────────┐
        │  Phase 2: Product Review          │ ◄── (Relational Store / SQLite / Summary)
        │  Sentiment & Experience Extraction│     Look up top reviews by `parent_asin`
        └───────────────────────────────────┘
```


#### Phase 1: Product Catalog Vector Search (ChromaDB)
Build a primary vector collection containing **only** product documents from `raw_meta`.
* **Vector Payload**: `Title + Features + Subfeatures + Description`
* **Metadata Fields**: `parent_asin`, `store`, `price`, `average_rating`, `rating_number`
* **Purpose**: Handles semantic matching and structured metadata pre-filtering (e.g., *"Find waterproof tents under $200"*).

#### Phase 2: User Experience & Review Enrichment (SQLite / Lookup Layer)
Store customer reviews in a lightweight, disk-backed relational database (such as SQLite) indexed by `parent_asin`.
* **Workflow**: Once ChromaDB returns top-matching `parent_asin` product IDs in Phase 1, query the relational database to fetch relevant review snippets (e.g., `SELECT text FROM reviews WHERE parent_asin = 'B004J2GUOU' ORDER BY helpful_vote DESC LIMIT 3;`).
* **Purpose**: Provides real-world context, user sentiment, and social proof to your LLM without bloating vector storage or degrading search accuracy.