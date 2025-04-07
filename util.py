"""
util.py

Desc:       utilities for Clique and Graph
Author:     jtpeller
Date:       2025.04.01
"""

# standard imports
import logging
import os
from pathlib import Path


def get_files_from_dir(d: str, ext: str) -> list[str]:
    """
    Returns a list of all files inside directory $d with extension $ext
    """
    results = []
    for f in os.listdir(d):
        if f.endswith(ext):
            results.append(f)
    return results


def check_create_dir(d: str, name: str = None, logger: logging.Logger = None):
    """
    Creates the directory if it doesn't exist. Logs @ info level using $logger.
    If it already exists, logs a debug.
    Name is used for logging; to specify directory's name for users.

    Returns:
        True if the dir was created, False otherwse.
    """
    if name is None:
        name = d
    if not os.path.exists(d):
        if logger:
            logger.info("[*] Creating %s directory...", name)
        os.mkdir(d)
        return True
    else:
        if logger:
            logger.debug(
                "[*] %s directory already exists.", name.capitalize())
        return False


def check_dir(d: str):
    """
    Returns true if $d exists and is a dir. False otherwise.
    """
    return Path(d).exists() and Path(d).is_dir()


def read_file(filepath: str):
    """
    Returns the contents of the .txt file at $filepath line-by-line. Line endings are stripped!
    Returns: 
        - List[str] for filepath contents. One line per list entry.
        - None if file doesn't exist, or is not a .txt file.
    """
    # error checks
    # ... check exists
    if not Path(filepath).exists():
        raise FileNotFoundError(
            f"[***] ERROR: File {filepath} does not exist.")

    # ... check that it's a text file
    if not filepath.endswith(".txt"):
        raise ValueError("[***] ERROR: File must be .txt")

    # read in file contents line-by-line.
    contents = []
    with open(filepath, 'r', encoding="utf-8") as f:
        for row in f:
            contents.append(row.strip())

    # return contents of file
    return contents
