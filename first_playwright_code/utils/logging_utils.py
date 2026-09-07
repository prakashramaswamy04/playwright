from datetime import datetime
import logging
from pathlib import Path


def configure_run_logging() -> tuple[logging.Logger, logging.FileHandler]:
    """Create a new timestamped log file for the current run."""
    logs_folder = Path(__file__).resolve().parents[1] / "logs"
    logs_folder.mkdir(parents=True, exist_ok=True)
    log_file = logs_folder / f"run_{datetime.now():%Y%m%d_%H%M%S_%f}.log"
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    ))
    root_logger.addHandler(file_handler)
    return root_logger, file_handler
