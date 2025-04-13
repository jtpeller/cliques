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
    Returns the list of all files inside directory $d with extension $ext

    Parameters
    ----------
    d : str
        Directory from which to retrieve the file-list.
    ext : str
        File extension. Can include the dot ('.txt'), but not required.

    Returns
    -------
    list[str]
        list of file path strings.
    """
    results = []
    for f in os.listdir(d):
        if f.endswith(ext):
            results.append(f)
    return results


def pop_without_remove(s: set):
    """
    Returns the result of s.pop() without actually removing the value from the set.

    Parameters
    ----------
    s : set
        The set to from which to retrieve the value.

    Returns
    -------
    Any
        Type of set element. Value is what would be the hypothetical "s[0]"
    """
    if not isinstance(s, set) or len(s) <= 0:
        return None
    for x in s:
        break
    return x


def check_create_dir(d: str, name: str = None, logger: logging.Logger = None):
    """
    Creates the directory if it doesn't exist. Logs @ info level using $logger.
    If it already exists, logs a debug.
    Name is used for logging; to specify directory's name for users.

    Parameters
    ----------
    d : str
        Directory to check / create.
    name : str, optional
        Name of the folder for logging. If None, set to d. By default None
    logger : logging.Logger, optional
        logging.Logger to be used for logging, if desired. By default None

    Returns
    -------
    bool
        Whether the directory was created (True) or not (False).
    """

    if name is None:
        name = d

    if not os.path.exists(d):
        if logger:
            logger.info("[*] Creating %s directory...", name)
        os.mkdir(d)
        return True

    if logger:
        logger.debug(
            "[*] %s directory already exists.", name)
    return False


def check_dir(d: str):
    """
    Assess $d and ensure it is an existing directory.

    Parameters
    ----------
    d : str
        Directory path to check.

    Returns
    -------
    bool
        True if $d exists and is a dir. False otherwise.
    """
    return Path(d).exists() and Path(d).is_dir()


def read_file(filepath: str):
    """
    Reads the file at $filepath line-by-line.

    Parameters
    ----------
    filepath : str
        filepath to read. Can be absolute or relative.

    Returns
    -------
    list[str]
        Contents of the file. Each line is a list entry.

    Raises
    ------
    FileNotFoundError
        If file at the filepath provided does not exist.
    ValueError
        If file at the filepath is not a .txt
    """
    # error checking
    # ... exists
    if not Path(filepath).exists():
        raise FileNotFoundError(
            f"[***] ERROR: File {filepath} does not exist.")

    # ... text file
    if not filepath.endswith(".txt"):
        raise ValueError("[***] ERROR: File must be .txt")

    # read in file contents line-by-line.
    contents = []
    with open(filepath, 'r', encoding="utf-8") as f:
        for row in f:
            contents.append(row.strip())

    # return contents of file
    return contents
