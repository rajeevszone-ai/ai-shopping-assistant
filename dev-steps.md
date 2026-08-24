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