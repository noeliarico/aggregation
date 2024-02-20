import os
import dotenv
import logging

dotenv.load_dotenv()


def get_disk_path() -> str:
    """
    Load the path to the disk where the profiles are stored.
    If no path is provided in the .env file, the default path is "localDB".

    If the directory does not exist, it is created.

    :return: str
    """
    disk_path = "localDB"

    if os.getenv("DISK_PATH") is not None:
        disk_path = os.getenv("DISK_PATH")

    # Check if the directory exists
    if not os.path.exists(disk_path):
        os.makedirs(disk_path)
        logging.warning(f"Directory {disk_path} did not exist. It has been automatically created.")

    return disk_path
