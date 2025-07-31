from dotenv import load_dotenv
import os

def get_env(var_name: str) -> str:
    load_dotenv()
    value: str | None = os.getenv(var_name)
    if not value:
        raise ValueError(f"{var_name} is not set in the environment variables.")
    return value