from dotenv import load_dotenv
import os

def get_private_app_key() -> str:
    load_dotenv()
    PRIVATE_APP_KEY: str | None = os.getenv("PRIVATE_APP_KEY")
    if not PRIVATE_APP_KEY:
        raise ValueError("PRIVATE_APP_KEY is not set in the environment variables.")
    return PRIVATE_APP_KEY