"""
This gets added to main, and gets called early.
"""
from __future__ import annotations

from os import getenv

from load_env_file import load_dotenv_if_present

def main() -> int:
    # Loads your .env into ENVIRONMENT if it exists.
    load_dotenv_if_present()


    # From .env.example
    # NAME_OF_ENV=development

    # Grab envs like so:
    NAME_OF_VARIABLE = getenv("NAME_OF_ENV")
    # NAME_OF_VARIABLE == "development"

    # Continue program ...

    return 0
