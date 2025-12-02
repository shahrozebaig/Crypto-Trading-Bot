import logging
import os
from logging.handlers import RotatingFileHandler

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, "bot.log")

logger = logging.getLogger("crypto_bot")
logger.setLevel(logging.DEBUG)

if logger.hasHandlers():
    logger.handlers.clear()

fmt = logging.Formatter(
    "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)

fh = RotatingFileHandler(LOG_FILE, maxBytes=2_000_000, backupCount=3)
fh.setFormatter(fmt)
fh.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setFormatter(fmt)
ch.setLevel(logging.INFO)

logger.addHandler(fh)
logger.addHandler(ch)

def setup_logger():
    logger.info("Logger initialized successfully")
