from __future__ import annotations

from pathlib import Path

def load_dotenv_if_present() -> int:
    """
    Dev convenience: load repo-root .env if python-dotenv is installed
    In production /docker, prefer real environment variables

    @Returns
    - 1 if .env file was loaded, 0 otherwise
    """
    try:
        from dotenv import load_dotenv #type: ignore[import-not-found]
    except ImportError:
        return 0

    here = Path(__file__).resolve()
    for rootpath in (here.parent, *here.parents):
        if (rootpath / "pyproject.toml").exists():
            envfile = rootpath / ".env"
            if envfile.exists():
                load_dotenv(dotenv_path = envfile, override=False)
                return 1
            break
    return 0
