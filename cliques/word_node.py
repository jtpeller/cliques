"""
Description
-----------
Implementation for WordNode class.

Metadata
--------
- Date: 2025.04.01
"""

# Standard
from dataclasses import dataclass


@dataclass
class WordNode:
    """
    A node in the graph.

    Attributes
    ----------
    word : str
        the word itself
    char_set : set[str]
        the set of characters in the word
    neighbors : set[int]
        the set of indices of neighboring words
    """

    word: str
    char_set: set[str]
    neighbors: set[int]
