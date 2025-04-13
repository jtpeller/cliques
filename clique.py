"""
clique.py

Desc:       Implementation for the Clique class
Author:     jtpeller
Date:       2025.04.01
"""

# standard
import copy
import csv
import logging
import sys
import time

# local imports
from graph import Graph
from word_node import WordNode
import util

# TODO: figure out how to make this a module / package for pip!


class Clique:
    """ Computes cliques using a word graph """
    MAX_LEN: int = 26

    def __init__(self,
                 words: list[str],
                 delim: str = ',',
                 fuzzy: bool = True,
                 log_level=logging.INFO):
        """
        Initializes Clique object.

        Parameters
        ----------
        words : list[str]
            the word list to be used to search for cliques.
        delim : str, optional
            CSV delimiter, by default ','
        fuzzy : bool, optional
            Whether to fuzzy search or not. 
            False gives strict cliques only (no repeated letters)
            True enables vowels to overlap at most once.
            By default False
        log_level : int, optional
            Logging level for Python's logging package.
            By default logging.INFO
        """
        # save input values
        self.words = words
        self.fuzzy = fuzzy
        self.delim = delim

        # setup for later calculations
        self.graph: Graph
        self.nodes: list[WordNode]
        self.cliques: list[int]
        self.word_cliques: list[str]
        self.length: int

        # logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger("Clique")
        self.logger.setLevel(log_level)

    def compute_cliques(self, length: int = 5):
        """
        Finds all cliques utilizing the provided word list for words of length specified by length.

        Cliques will be limited by a specific factor: alphabet size. Assumes English, so 26 letters.
            - All cliques of words with length 5 must have 5 words in the clique, as 5x5=25.
            - All cliques of words with length 6, then 4 words. (24 letters total).
            - 7 -> 3 words (21 letters), and so on.

        Graphs are utilized to set up the "neighbors" of each word. Neighbors are those words 
        with which the current word has no letters in common. (e.g., "fjord" and "waltz")

        If no cliques are found, then another method can be used: fuzzy search. 
        This allows some overlap in the cliques.

        Raises
        ------
        ValueError
            If length is not between 1 and 26.
        """
        # error checks
        # ... length is a positive number between 1 and 26.
        if not isinstance(length, int) or length <= 0 or length > 26:
            raise ValueError(
                f"[***] ERROR: Length must be a number between 1 and 26. Got: {length}")

        # save attribute
        self.length = length

        # create graph
        g_start = time.time()
        self.logger.info("[*] Computing Graph for length %d...", length)
        self.graph = Graph(words=self.words, length=length,
                           fuzzy=self.fuzzy, log_level=self.logger.getEffectiveLevel())
        self.graph.compute_graph()
        self.nodes = self.graph.nodes   # bring it up a level due to laziness
        g_comp = time.time() - g_start
        self.logger.info("[*] Graphs computed in %.3f seconds.", g_comp)

        # compute cliques
        c_start = time.time()
        self.logger.info(
            "[*] Computing all cliques for length %d. This may take a while...", length)

        # ... compute the cliques
        self.cliques = self._get_clique_list(length)
        cliques_found = len(self.cliques)
        if cliques_found == 0:
            self.logger.info("[*] No cliques found.")

        # ... convert indexes to words
        self._get_word_repr()

        # ... log
        c_comp = time.time() - c_start
        self.logger.info("[*] Cliques computed in %.3f seconds.", c_comp)

        # exit log
        self.logger.info(
            "[*] Total Execution Time: %.3f seconds.", c_comp + g_comp)

    def write_cliques(self, filepath: str):
        """
        Writes this object's cliques to file at CSV. Will overwrite.

        Parameters
        ----------
        filepath : str
            the filepath to write.
        """
        if len(self.word_cliques) == 0:
            self.logger.debug("[*] Skipping write-to-file. No cliques.")
            return

        # generate dict format
        output: list[dict] = []
        for cliq in self.word_cliques:
            repeats, missing = self._get_repeats_and_missing(cliq)
            output.append({
                "Clique": cliq,
                "Fuzzy": len(repeats) > 0,
                "Repeats": repeats,
                "Missing": missing
            })
        fn = list(output[0].keys())

        # open and write.
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fn, delimiter=self.delim)
            writer.writeheader()
            writer.writerows(output)

    #########################################
    #           HELPER FUNCTIONS            #
    #########################################

    def _clique_layer_t(self, n: int, prev_idx: list[int], prev_n: set[int], cl: list[list[int]]):
        """ generalizes the clique case to enable n-level clique computation. """
        # error checking
        # ... n must be a non-negative int!
        if not isinstance(n, int) or n < 2:
            raise ValueError(f"[***] n must be an int larger than 1. Got: {n}")

        # ... warn about n being too large
        if n > 8:
            self.logger.warning(
                "[**] WARNING: n > 8 means you have word length of 2. I recommend not doing this.")

        # handle if n < 3 (i.e., you want a clique of 2 words)
        if n == 2:
            self._clique_loop_end(cl, prev_idx, prev_n)
            return      # no need to execute further. this is a base case!

        # now, run through the general algorithm
        for next_idx in prev_n:
            if next_idx < prev_idx[-1]:
                continue

            # remaining candidates will be in intersection:
            next_n = prev_n & self.nodes[next_idx].neighbors

            # # # BASE CASE # # #

            # if n-2 is 1 (i.e., n is 3 or lower for robustness), then we need to call the loop end
            # this represents the last "layer" of words to add to the clique.
            if n <= 3:        # or, n <= 3
                idx_copy = copy.copy(prev_idx)
                idx_copy.append(next_idx)
                self._clique_loop_end(cl, idx_copy, next_n)
                return      # loop is over!

            # check if number of neighbors in next_n is large enough
            if len(next_n) < (n-2):
                continue

            # call the next layer (recursively)
            idx_copy = copy.copy(prev_idx)
            idx_copy.append(next_idx)
            self._clique_layer_t(n-1, idx_copy, next_n, cl)

    def _clique_loop_end(self, cl: list[list[int]], prev_idx: list[int], prev_n: set[int]):
        """ represents the final loop, where all clique indexes are aggregated. """
        prev = prev_idx[-1]
        for r in prev_n:
            if r < prev:
                continue
            prev_copy = copy.deepcopy(prev_idx)
            prev_copy.append(r)
            cl.append(prev_copy)

    def _get_clique_list(self, length: int):
        """
        Interface function to call the specific helper function to find how many cliques.

        Parameters
        ----------
        length : int
            What word length of the list is being calculated.

        Returns
        -------
        list[int]
            List of cliques. Each entry in this list are the indexes into self.nodes
        """

        # first, determine which clique length must be chosen
        # example: 26 / 5 = 5.2 -> int(5.2) -> 5
        num_words = int(self.MAX_LEN / length)
        self.logger.debug("[*] Computing cliques of %d words...", num_words)

        cl = []
        for i, node in enumerate(self.nodes):
            ni = node.neighbors
            # call the clique template function with num_words
            self._clique_layer_t(n=num_words, prev_idx=[i], prev_n=ni, cl=cl)
        return cl

    def _get_repeats_and_missing(self, words: list[str]) -> tuple[list[str], list[str]]:
        """
        Discovers any letters across all the words in $cliq that are repeats.
        Also computes any omitted letters!

        Parameters
        ----------
        cliq : list[str]
            list of words

        Returns
        -------
        list[str]
            list of repeated letters
        """
        # first count up all letters
        d = dict(zip("abcdefghijklmnopqrstuvwxyz", [0]*26))
        for word in words:
            for letter in word:
                d[letter.lower()] += 1      # frequency count

        # then, create a list of repeated (freq > 1) and missing (freq == 0) letters
        repeats = []
        missing = []
        for k, v in d.items():
            if v > 1:
                repeats.append(k)
            elif v == 0:
                missing.append(k)
        return repeats, missing

    def _get_word_repr(self):
        """
        Utilizes self.cliques (which has the indexes) to 
        generate self.word_cliques (which will have the words).
        """
        # loop through every clique
        self.word_cliques = []
        for wc_idx, cliq in enumerate(self.cliques):
            self.word_cliques.append([])

            # loop through every word in cliq
            for idx in cliq:
                self.word_cliques[wc_idx].append(self.nodes[idx].word)


if __name__ == "__main__":
    # read in words
    all_words = util.read_file("./words/output.txt")
    FUZZY_ONLY = True

    # set up clique output dir
    OUT_DIR = "Cliques"
    util.check_create_dir(OUT_DIR)

    # compute Cliques!
    cliques = Clique(words=all_words, delim=",", fuzzy=True)
    for word_len in range(3, 13):
        cliques.compute_cliques(word_len)

        FP = f'{OUT_DIR}/cliques-{word_len}.csv'
        cliques.write_cliques(FP)

    sys.exit(0)
