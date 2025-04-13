"""
graph.py

Desc:       Implementation for the Graph class
Author:     jtpeller
Date:       2025.04.01
"""

# standard imports
import csv
import logging
import time

# local imports
from word_node import WordNode
from util import pop_without_remove as pop_wr


class Graph:
    """
    Graph data structure.
    """

    def __init__(self,
                 words: list[str],
                 length: int,
                 fuzzy: bool = False,
                 log_level: int = logging.INFO):
        """
        Constructs and partially initializes a Graph.

        Parameters
        ----------
        words : list[str]
            List of words. Should be same length, and stripped (not required).
        length : int
            Length of the words from the list to be computed. 
            Allows providing a list of words with variable length, but only want to compute
            those with length 5, for instance.
        fuzzy : bool, optional
            Controls whether fuzzy search is used. Useful when list may not have an explicit clique.
            By default False
        log_level : int, optional
            Controls logger's log level, by default logging.INFO

        Raises
        ------
        ValueError
            Thrown if words is not provided, or malformed (like [])
        ValueError
            Thrown if length is not provided, or malformed (like length = 4.2)
        """
        # error checking
        # ... words must be provided.
        if len(words) <= 0 or words is None:
            raise ValueError(f"Words must be a list of words, but got {words}")

        # ... if length is not provided, that is OK
        if not isinstance(length, int) or length is None:
            raise ValueError(f"Length must be an int, but got {length}")

        # save remaining values
        self.words = words
        self.fuzzy = fuzzy
        self.length = length

        # to be created
        self.nodes: list[WordNode] = []

        # create logger
        self.logger = logging.getLogger("Graph")
        self.logger.setLevel(log_level)

        # initialize nodes with words list
        self._init_nodes()

    def compute_graph(self):
        """
        Computes each node's neighbors. Call this to actually build the graph.

        When fuzzy search is active, allows for vowels to overlap, enabling cliques to be found
        for situations where there otherwise would be no existing cliques (e.g., for a clique 
        of words with length 3, which requires 8 words, but there are only 5 vowels!).

        When fuzzy search is disabled, only strict cliques are found, where all letters are unique
        """
        start = time.time()

        # max fuzzy count per node
        max_fuzzy = 3

        # compute neighbors for each word; other words which have distinct letters
        for node in self.nodes:
            # extract node attributes.
            char_set = node.char_set
            neighbors = node.neighbors

            # count how many fuzzy interactions
            n_fuzzy = 0
            vowels_left = "aeiou"

            # iterate over all words again
            for j in self.nodes:
                # only add neighbors if they aren't duplicates.
                intersection = char_set & j.char_set
                if len(intersection) == 0:
                    neighbors.add(self._get_word_index(j.word))
                elif self.fuzzy \
                        and len(intersection) == 1 \
                        and pop_wr(intersection) in vowels_left \
                        and n_fuzzy < max_fuzzy:
                    neighbors.add(self._get_word_index(j.word))
                    vowels_left.replace(pop_wr(intersection), "")
                    n_fuzzy += 1

        # output
        self.logger.info(
            '[*] Graph creation complete in %.3f seconds', time.time() - start)

    def write_graphs(self, output_dir: str, delim: str = ","):
        """
        Writes graphs to a CSV file in output dir.

        Default filepath is f'{output_dir}/word_graph-{self.length}.csv

        Single line format is: word,fuzzy,[neighbors[0], neighbors[1], ..., neighbors[-1]]

        Parameters
        ----------
        output_dir : str
            What directory the file should be written to.
        delim : str, optional
            CSV delimiter. By default ","
        """

        # setup filename based on fuzziness
        filepath = f'{output_dir}/word_graph-{self.length}.csv'

        # open file & write
        self.logger.info('[*] Writing to %s', filepath)
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f, delimiter=delim)
            for node in self.nodes:
                writer.writerow(
                    [node.word, self.fuzzy, str(list(sorted(node.neighbors)))])

    def _init_nodes(self):
        """ utilizes self.words to populate self.nodes. """

        # loop over every word
        for word in self.words:
            # extract the word and remove the newline
            word = word.strip()

            # only utilize words of specified length
            if len(word) != self.length:
                continue

            # compute set representation of the word (i.e. the set of characters)
            char_set = set(word)

            # this word contains duplicate letters. move on
            if len(char_set) != self.length:
                continue

            # append the WordNode. Empty set since neighbors is computed later
            self.nodes.append(
                WordNode(word=word, neighbors=set(), char_set=char_set))

    def _get_word_index(self, word: str):
        """
        Finds the index of word in the node list.

        Parameters
        ----------
        word : str
            word to lookup.

        Returns
        -------
        int, None
            Returns idx of word if found. None otherwise.
        """
        for idx, node in enumerate(self.nodes):
            if node.word == word:
                return idx
        return None
