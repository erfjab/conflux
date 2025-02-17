import os
import json
import asyncio

from app.settings import logger, env
from app.api import ApiManager
from app.utils import clear_terminal, modify_user_data


async def main():
    clear_terminal()
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



    for user in users:
        for user in users:
            userdata = modify_user_data(user=user)
            created_user = await api.modify_user(
                data=userdata, access=token.access_token
            )
            if not created_user:
                logger.error(f"User `{user.get('username')}` is not created!")
                continue


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.warning("Process interrupted by user. Exiting...")
    except Exception as e:
        logger.critical(f"Unexpected error occurred: {str(e)}")
