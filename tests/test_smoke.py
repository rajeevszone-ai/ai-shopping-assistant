from shopping_assistant import __version__
from shopping_assistant.main import main


def test_package_has_version() -> None:
    assert __version__ == "0.1.0"


def test_main_reports_ready(capsys) -> None:
    main()

    assert capsys.readouterr().out == "AI Shopping Assistant is ready.\n"
