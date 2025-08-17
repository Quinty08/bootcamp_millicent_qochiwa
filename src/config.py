from dotenv import load_dotenv
import os
from pathlib import Path

def load_env(env_path: str = None):
    """Load .env from project root or explicit path."""
    if env_path:
        load_dotenv(env_path)
    else:
        load_dotenv()

def get_key(name: str, default=None):
    return os.getenv(name, default)

def data_dir():
    return Path(os.getenv("DATA_DIR", "./data"))
