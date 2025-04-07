"""
word_node.py

Desc:       Implementation for WordNode class.
Author:     jtpeller
Date:       2025.04.01
"""

from dataclasses import dataclass


@dataclass
class WordNode:
    """
    A node in the graph.

    Attributes:
        word: str
            - the word itself
        char_set: set[str]
            - the set of characters in the word
        neighbors: set[int]:
            - the set of indices of neighboring words
    """
    word: str
    char_set: set[str]
    neighbors: set[int]
