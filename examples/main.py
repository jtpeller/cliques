import logging
import os

from cliques.clique import Clique
from cliques.util import CliqueUtils

if __name__ == "__main__":
    # Set up logging, if you desire.
    logging.basicConfig(level=logging.INFO)

    # Read in words. You may utilize the built-in method, or you may utilize your own.
    # As long as the word list is available in a Python list, this will work perfectly.
    root_path = os.path.dirname(os.path.realpath(__file__))
    all_words = CliqueUtils.read_file(f"{root_path}/words/output.txt")
    FUZZY_ONLY = True

    # Set up clique output dir
    output_dir = "Output"
    CliqueUtils.mkdir(output_dir)

    # Compute Cliques!
    cliques = Clique(words=all_words, delim=",", fuzzy=True)
    for word_len in range(3, 13):
        cliques.compute_cliques(word_len)

        file_path = f"{output_dir}/cliques-{word_len}.csv"
        cliques.write_cliques(file_path)
