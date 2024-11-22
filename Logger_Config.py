# logger_config.py
import logging
import os


def setup_logger(name, log_file, level=logging.INFO):
    # Create a logger
    logger = logging.getLogger(__name__)
    logger.setLevel(level)

    # Create the logs directory if it does not exist
    log_dir = os.path.dirname(log_file)
    os.makedirs(log_dir, exist_ok=True)

    # Create handlers (e.g., console and file handlers)
    console_handler = logging.StreamHandler()
    file_handler = logging.FileHandler(log_file)

    # Set levels for handlers
    console_handler.setLevel(level)
    file_handler.setLevel(level)

    # Create formatters and add them to handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    # Add handlers to the logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger