import datetime
import os
from enum import Enum, StrEnum
from pathlib import Path

from dotenv import load_dotenv
from loguru import logger


class MessageType(Enum):
    NONE = "none"
    FILE_DEBUG = "file_debug"
    SUCCESS = "success"
    WARNING = "warning"
    ERROR = "error"


class ColorCode(StrEnum):
    RESET = "\033[0m"
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"

load_dotenv()
LOG_DIR = os.getenv("LOG_DIR")
if LOG_DIR is not None:
    # (Normal case)
    # Since we have LOG_DIR, we will create files in LOG_DIR and output there

    # make sure the log dir exists
    log_dir_path = Path(LOG_DIR)
    log_dir_path.mkdir(exist_ok=True)

    # On program start, create a new log file
    timestamp = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    for log_level in ["ERROR", "INFO", "DEBUG"]:
        log_file_name = f"{timestamp}.{log_level}"
        rotated_log = log_dir_path / log_file_name

    logger.remove()
    logger.add(log_dir_path / f"{timestamp}.DEBUG", format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{line} | {message}", level="DEBUG")
    logger.add(log_dir_path / f"{timestamp}.INFO", format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{line} | {message}", level="INFO")
    logger.add(log_dir_path / f"{timestamp}.ERROR", format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{line} | {message}", level="ERROR")
else:
    # (Unit test)
    print("LOG_DIR environment variable is not set! Print to console instead.")

def _message_type_to_color(msg_type: MessageType) -> str:
    if msg_type == MessageType.NONE:
        return str(ColorCode.RESET)
    elif msg_type == MessageType.SUCCESS:
        return str(ColorCode.GREEN)
    elif msg_type == MessageType.WARNING:
        return str(ColorCode.YELLOW)
    elif msg_type == MessageType.ERROR:
        return str(ColorCode.RED)
    else:
        raise ValueError(f"Unknown message type: {msg_type}")

def log_debug(log_str: str, exc: Exception | None = None) -> None:
    logger.opt(depth=1, exception=exc).debug(log_str)

def log_info(log_str: str, exc: Exception | None = None) -> None:
    logger.opt(depth=1, exception=exc).info(log_str)

def log_error(log_str: str, exc: Exception | None = None) -> None:
    logger.opt(depth=1, exception=exc).error(log_str)
