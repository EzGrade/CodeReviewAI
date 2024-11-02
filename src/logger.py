"""
This module is responsible for creating and configuring the logger.
"""

import logging
import config

logging.basicConfig(
    level=logging.getLevelName(config.LOGGING_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("/var/log/web/logs.log"),
        logging.StreamHandler()
    ]
)


def get_logger(name: str) -> logging.Logger:
    """
    Function to get the logger
    :param name:
    :return:
    """
    return logging.getLogger(name)
