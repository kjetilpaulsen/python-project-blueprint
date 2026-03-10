"""
This gets added to main, and gets called early. 
"""
from __future__ import annotations

from paths import get_app_paths, ensure_dirs



def main() -> int:
    # Call this to get all the paths you need, swap the name from myapp
    paths = get_app_paths("myapp")
    # Create the dirs
    ensure_dirs(paths)

    # Continue program ...

    return 0
