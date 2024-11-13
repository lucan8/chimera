import os
import re
import numpy as np
from collections import Counter

from typing import Tuple, Dict, List, Set


def flatten(dir_path: str, ext: str) -> Set[str]:
    """
    `flatten` walks the dir_path tree and inserts the files that match the
    file extension into a set, if the entry is a directory then it will
    create a recursive call to flatten every directory it encounters
    and will unite everything into a set.
    Additionally, a random percentage of the files will be saved in order to
    be tested upon
    """
    files = set()
    for dirpath, dirnames, filenames in os.walk(dir_path):
        files.update({os.path.join(dirpath, f) for f in filenames if f.endswith("." + ext)})
        #Going through the remaining the directories
        for dirname in dirnames:
            files.update(flatten(os.path.join(dirpath, dirname), ext))

    return files


def extract_data(keywords: List[str], dir_path: str, ext: str) -> Tuple[Dict[str, int], int, int]:
    """
    `extract_dat` walks the given directory path to look for files that end
    in `.{ext}`, if it encounters another directory it will recursively process
    that direcotry and combines the return data with the data in the main call.
    """
    keyword_frq = {keyword: 0 for keyword in keywords}
    lang_files = flatten(dir_path, ext)

    # split into training and test
    percentage_test = 0.2
    test_files = np.random.choice(list(lang_files), size=int(len(lang_files) * percentage_test), replace=False)
    lang_files.difference_update(test_files)
    with open("resources/tests.txt", "a") as tests:
        for file in test_files:
            tests.write(f"{file} {ext}\n")

    print(f"Sampling {len(lang_files)} '{ext}' files...")

    for f_lang in lang_files:
        try:
            with open(f_lang, "r") as file:

                # We have to do this to make sure we don't miss cases such as:
                # We will have to split by multiple characters to account for
                # inconsistencies such as:
                # 1. `template<class T>` instead of `template <class T>
                # 2. `vector<vector<T>>`

                # TODO: more separators to be found for a more accurate tokens

                is_multiline_comment = False
                for line in file:
                    #Checking for start of multiline comment
                    if line.find("/*") != -1:
                        is_multiline_comment = True

                    # Getting index of end of multiline comment char
                    comment_end = line.find("*/")
                    # Setting the flag as false and replacing the line with the reamining part without comment
                    if comment_end != -1:
                        is_multiline_comment = False
                        line = line[comment_end + 1:]

                    #If the flag is set to true we just ignore the line, otherwise we parse it
                    if not is_multiline_comment:
                        #ignoring single line comments
                        comment_start = line.find("//")
                        if comment_start != -1:
                            line = line[0:comment_start]

                        # Spliting the tokens into a frequency dictionary
                        tokens = Counter(re.split(r'[ \t\n<>(){}!=*;:,|^%]+', line))

                        # Adding the frequency of the tokens to keyword_freq
                        for token, nr_tokens in tokens.items():
                            if token in keyword_frq:
                                keyword_frq[token] += nr_tokens
        except (IOError, OSError, UnicodeDecodeError) as e:
            print(f"Failed to open: {f_lang}")
            continue

    return keyword_frq, sum(keyword_frq.values()), len(lang_files)


def main():
    samples = ["cpp", "java", "rs"]

    # delete contents of tests
    with open("resources/tests.txt", "w") as file:
        pass

    keywords = []
    with open("resources/keywords.txt", "r") as file:
        for line in file:
            words = line.split()
            keywords.extend(words)

    for file_extension in samples:
        keywords_frq, total_tokens, total_files = extract_data(keywords, "samples/", file_extension)

        results_file = "results/" + file_extension + "_results.txt"
        with open(results_file, "w") as file:
            file.write(f"{total_tokens} {total_files}\n")

            for key in keywords_frq:
                file.write(f"{key} {keywords_frq[key]}\n")
main()
