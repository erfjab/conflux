import os
import asyncio

from app.settings import logger, env
from app.api import ApiManager


async def main():
    logger.info("Starting Import Process...")

    # Check if 'export.json' exists
    if not os.path.exists("export.json"):
        logger.critical(
            "File 'export.json' not found. Please ensure it exists before running the script."
        )
        exit(1)
    logger.info("File 'export.json' found successfully.")

    # Check if environment configuration is valid
    if not env.import_is_config():
        logger.critical(
            "Environment configuration is missing. Please check the .env file."
        )
        exit(1)
    logger.info("Environment configuration loaded successfully.")

    # Validate host configuration
    try:
        env.validate_host(env.EXPORT_HOST)
        logger.info("Host configuration validated successfully.")
    except ValueError as e:
        logger.error(f"Invalid host configuration: {str(e)}. Exiting...")
        exit(1)

    # Initialize API Manager and Attempt to retrieve token
    try:
        api = ApiManager(host=env.IMPORT_HOST)
        token = await api.get_token(
            username=env.IMPORT_USERNAME, password=env.IMPORT_PASSWORD
        )
        if not token:
            logger.critical(
                "Failed to retrieve token. Please check your username/password."
            )
            exit(1)
        logger.info("Connecting to API and Token retrieved successfully.")
    except Exception as e:
        logger.error(f"Error while retrieving token: {str(e)}")
        exit(1)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.warning("Process interrupted by user. Exiting...")
    except Exception as e:
        logger.critical(f"Unexpected error occurred: {str(e)}")
