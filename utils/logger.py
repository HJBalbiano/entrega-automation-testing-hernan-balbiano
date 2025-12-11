import logging
from pathlib import Path
from typing import Optional

from utils.data_loader import ensure_dir


LOG_DIR = Path("artifacts") / "logs"
ensure_dir(LOG_DIR)


def create_logger(name: str, log_file: Optional[str] = None) -> logging.Logger:
    """Create or retrieve a configured logger."""
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)
    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(name)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Console handler
    console = logging.StreamHandler()
    console.setFormatter(formatter)
    logger.addHandler(console)

    # File handler
    log_path = Path(log_file) if log_file else LOG_DIR / f"{name}.log"
    ensure_dir(log_path.parent)
    file_handler = logging.FileHandler(log_path, encoding="utf-8")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    logger.propagate = False
    return logger
