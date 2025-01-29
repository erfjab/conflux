import os
import json
import asyncio

from app.settings import logger, env
from app.api import ApiManager


async def main():
    logger.info("Starting Import Process...")

    # Check if 'export.json' exists
    file_path = os.path.join(os.path.dirname(__file__), "export.json")
    if not os.path.exists(file_path):
        logger.critical(
            "File 'export.json' not found. Please ensure it exists before running the script."
        )
        exit(1)
    logger.info("File 'export.json' found successfully.")

    # Load users from 'export.json'
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            users: list[dict] = json.load(f)
    except Exception as e:
        logger.critical(f"Failed to read 'export.json': {str(e)}")
        exit(1)

    if not isinstance(users, list):
        logger.critical(
            "Invalid data format in 'export.json'. Expected a list of users."
        )
        exit(1)

    # Check if environment configuration is valid
    if not env.import_is_config():
        logger.critical(
            "Environment configuration is missing. Please check the .env file."
        )
        exit(1)
    logger.info("Environment configuration loaded successfully.")

    # Validate host configuration
    try:
        env.validate_host(env.IMPORT_HOST)
        logger.info("Host configuration validated successfully.")
    except ValueError as e:
        logger.error(f"Invalid host configuration: {str(e)}. Exiting...")
        exit(1)

    # Initialize API Manager and retrieve token
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
        logger.info("Connected to API and token retrieved successfully.")
    except Exception as e:
        logger.error(f"Error while retrieving token: {str(e)}")
        exit(1)

    # Check users
    duplicates = []
    for user in users:
        username = user.get("username", None)
        if not username:
            logger.warning("Skipping user entry with missing 'username'.")
            continue

        try:
            existing_user = await api.get_user(
                username=username, access=token.access_token
            )
            if existing_user:
                duplicates.append(username)
                logger.info(f"User '{username}' already exists.")
        except Exception as e:
            logger.error(f"Error checking user '{username}': {str(e)}")

    # Show duplicates
    if duplicates:
        logger.info(f"Total duplicate users found: {len(duplicates)}")
        logger.info("| ".join(duplicates))
    else:
        logger.info("Nice, no duplicate users found.")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.warning("Process interrupted by user. Exiting...")
    except Exception as e:
        logger.critical(f"Unexpected error occurred: {str(e)}")
