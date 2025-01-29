import asyncio
from app.settings import logger, env
from app.api import ApiManager


async def main():
    logger.info("Starting Export Process...")

    # Check if environment configuration is valid
    if not env.is_config():
        logger.critical(
            "Environment configuration is missing. Please check the .env file."
        )
        exit(1)
    logger.info("Environment configuration loaded successfully.")

    # Validate host configuration
    try:
        env.validate_host()
        logger.info("Host configuration validated successfully.")
    except ValueError as e:
        logger.error(f"Invalid host configuration: {str(e)}. Exiting...")
        exit(1)

    # Initialize API Manager
    api = ApiManager(host=env.EXPORT_HOST)
    logger.info(f"Connecting to API at {env.EXPORT_HOST}...")

    # Attempt to retrieve token
    try:
        token = await api.get_token(
            username=env.EXPORT_USERNAME, password=env.EXPORT_PASSWORD
        )
        if not token:
            logger.critical(
                "Failed to retrieve token. Please check your username/password."
            )
            exit(1)
        logger.info("Token retrieved successfully.")
    except Exception as e:
        logger.error(f"Error while retrieving token: {str(e)}")
        exit(1)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.warning("⚠️ Process interrupted by user. Exiting...")
    except Exception as e:
        logger.critical(f"❌ Unexpected error occurred: {str(e)}")
