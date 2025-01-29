import asyncio
import json
from datetime import datetime

from app.settings import logger, env
from app.api import ApiManager
from app.utils import clear_terminal


# Custom JSON encoder to handle datetime serialization
class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)


async def main():
    clear_terminal()
    logger.info("Starting Export Process...")

    # Check if environment configuration is valid
    if not env.export_is_config():
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
        api = ApiManager(host=env.EXPORT_HOST)
        token = await api.get_token(
            username=env.EXPORT_USERNAME, password=env.EXPORT_PASSWORD
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

    # Export users with pagination
    offset = 0
    limit = 50
    all_users = []
    logger.info("Starting to retrieve users...")

    while True:
        try:
            users = await api.get_users(
                access=token.access_token, offset=offset, limit=limit
            )
            if not users:
                logger.info("All users retrieved successfully.")
                break

            all_users.extend([user.model_dump() for user in users])
            logger.info(
                f"Retrieved {len(users)} users (Offset: {offset}, Limit: {limit})."
            )

            offset += limit
        except Exception as e:
            logger.error(f"Error while retrieving users: {str(e)}")
            break

    # Save users to a JSON file
    if all_users:
        try:
            with open("export.json", "w", encoding="utf-8") as f:
                json.dump(
                    all_users, f, ensure_ascii=False, indent=4, cls=CustomJSONEncoder
                )
            logger.info(
                f"Successfully exported {len(all_users)} users to 'export.json'."
            )
        except Exception as e:
            logger.error(f"Error while saving users to file: {str(e)}")
    else:
        logger.warning("No users were retrieved to export.")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.warning("Process interrupted by user. Exiting...")
    except Exception as e:
        logger.critical(f"Unexpected error occurred: {str(e)}")
