import re
import math
from collections import defaultdict
from typing import Tuple, Dict, List, Set


# Count of each keyword in every category
# cpp_keywords, rust_keywords, java_keywords

# Count of total words in each category:
# cpp_total_words, java_total_words, rust_total_words

# Count of files found of each type:
# data_count, cpp_count, java_count, rust_count


# Read from the result file associated with each language
def read_from_results(file: str) -> Tuple[int, int, Dict[str, int]]:
    results_file = open(file, "r")
    total_words, count = [int(n) for n in results_file.readline().split()]
    keywords = defaultdict(int)
    for line in results_file.readlines():
        keywords[line.split()[0]] = int(line.split()[1])
    results_file.close()
    return total_words, count, keywords


cpp_total_words, cpp_count, cpp_keywords = read_from_results("results/cpp_results.txt")
java_total_words, java_count, java_keywords = read_from_results("results/java_results.txt")
rust_total_words, rust_count, rust_keywords = read_from_results("results/rs_results.txt")

data_count = cpp_count + java_count + rust_count

# Prior probabilities
p_cpp = cpp_count / data_count
p_java = java_count / data_count
p_rust = rust_count / data_count


# Calculate the conditional probabilities for each category
# smoothing refers to additive/Laplace smoothing
def calc_probabilities(word_dict: Dict[str, int], total_words: int, selected_words, smoothing: int = 1) -> Dict[str, float]:
    probabilities = dict()

    for keyword in selected_words:
        probabilities[keyword] = (word_dict.get(keyword, 0) + smoothing) \
            / (total_words + smoothing * len(selected_words))
    return probabilities

# Returns dicts with key as extension, value as a dictionary of keywords and probabilities
def getKeywordProbabilites(selected_words):
    return {"cpp": calc_probabilities(cpp_keywords, max(cpp_total_words, 1), selected_words),
            "java": calc_probabilities(java_keywords, max(java_total_words, 1), selected_words),
            "rs": calc_probabilities(rust_keywords, max(rust_total_words, 1), selected_words)
            }

def getSelectedWords():
    return " ".join(open("resources/keywords.txt", "r").readlines()).split()

# Returns most probable programming language for a file's data
def classify(data, selected_words):
    data_words = set(re.findall(r'\w+', data.lower()))

    """
    Log Probabilities:
    The conditional probabilities for each class given an attribute value are small.
    When they are multiplied together they result in very small values, 
    which can lead to floating point underflow. 
    A common fix for this is to add the log of the probabilities together
    """
    probabilites = {"cpp": math.log(p_cpp) if p_cpp else 0,
                    "java": math.log(p_java) if p_java else 0,
                    "rs": math.log(p_rust) if p_rust else 0}

    for ext, keywords_prob in getKeywordProbabilites(selected_words).items():
        for word in data_words:
                if word in selected_words:
                    probabilites[ext] += math.log(keywords_prob[word]) if keywords_prob[word] else 0
                

    # If there are no files of a specific type,
    # the final probability associated with the category will be 0
    probabilites = {ext: math.exp(prob) for ext, prob in probabilites.items()}
    return max(probabilites, key=probabilites.get)

