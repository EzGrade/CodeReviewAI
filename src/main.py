"""
Main module to run the application
"""
import uvicorn

import logger
from api.router import app

logger = logger.get_logger(__name__)


def main():
    """
    Function to run the application
    :return:
    """
    host = "0.0.0.0"
    port = 8000
    logger.info("Starting the application on %s:%s", host, port)
    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
