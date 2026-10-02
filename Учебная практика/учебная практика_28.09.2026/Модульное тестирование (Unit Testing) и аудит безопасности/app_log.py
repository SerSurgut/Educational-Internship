import logging
from pathlib import Path

LOG_FILE = Path(__file__).parent / "app.log"


def setup_logging():
    logging.basicConfig(filename=LOG_FILE, encoding="utf-8",
                        level=logging.ERROR,
                        format="%(asctime)s %(levelname)s %(message)s",
                        datefmt="%d.%m.%Y %H:%M:%S")


def log_error(text, error):
    details = " ".join(str(error).split())
    logging.error("%s: %s", text, details)
