import numpy as np
import matplotlib.pyplot as plt

import re
import math
from collections import defaultdict
from typing import Tuple, Dict, List, Set

# Get selected keywords (cpp, rust, java)
selected_words = " ".join(open("keywords.txt", "r").readlines()).split()

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


cpp_total_words, cpp_count, cpp_keywords = read_from_results("cpp_results.txt")
java_total_words, java_count, java_keywords = read_from_results("java_results.txt")
rust_total_words, rust_count, rust_keywords = read_from_results("rs_results.txt")

data_count = cpp_count + java_count + rust_count

# Prior probabilities
p_cpp = cpp_count / data_count
p_java = java_count / data_count
p_rust = rust_count / data_count


# Calculate the conditional probabilities for each category
# smoothing refers to additive/Laplace smoothing
def calc_probabilities(word_dict: Dict[str, int], total_words: int, smoothing: int = 1) -> Dict[str, float]:
    probabilities = dict()
    for keyword in selected_words:
        probabilities[keyword] = (word_dict.get(keyword, 0) + smoothing) \
            / (total_words + smoothing * len(selected_words))
    return probabilities


# In case there are no files of a specific type,
# we make TotalWords = 1 to avoid division by 0
keyword_probabilities_cpp = calc_probabilities(cpp_keywords, max(cpp_total_words, 1))
keyword_probabilities_java = calc_probabilities(java_keywords, max(java_total_words, 1))
keyword_probabilities_rust = calc_probabilities(rust_keywords, max(rust_total_words, 1))

def classify(data):
    data_words = set(re.findall(r'\w+', data.lower()))

    """
    Log Probabilities:
    The conditional probabilities for each class given an attribute value are small.
    When they are multiplied together they result in very small values, 
    which can lead to floating point underflow. 
    A common fix for this is to add the log of the probabilities together
    """
    cpp_probability = math.log(p_cpp) if p_cpp else 0
    java_probability = math.log(p_java) if p_java else 0
    rust_probability = math.log(p_rust) if p_rust else 0


    for word in data_words:
        if word in selected_words:
            cpp_probability += math.log(keyword_probabilities_cpp[word]) if keyword_probabilities_cpp[word] else 0
            java_probability += math.log(keyword_probabilities_java[word]) if keyword_probabilities_java[word] else 0
            rust_probability += math.log(keyword_probabilities_rust[word]) if keyword_probabilities_rust[word] else 0

    # If there are no files of a specific type,
    # the final probability associated with the category will be 0
    cpp_probability = math.exp(cpp_probability) if p_cpp else 0
    java_probability = math.exp(java_probability) if p_java else 0
    rust_probability = math.exp(rust_probability) if p_rust else 0

    res = [cpp_probability, java_probability, rust_probability]

    if max(res) == cpp_probability:
        return "cpp"
    elif max(res) == java_probability:
        return "java"
    else:
        return "rs"


# Draw a graph for showing results after testing the model
def draw_results_graph(files_found: List[int], files_total: List[int]) -> None:
    languages = ["C++", "Java", "Rust"]

    x = np.arange(len(languages))

    fig, ax = plt.subplots(figsize=(6, 4))

    plt.bar(languages, files_total, color='green', label="Expected")
    plt.bar(languages, files_found, color='blue', alpha=0.3, label="Found")

    plt.xlabel("Languages")
    plt.ylabel("Guesses")
    plt.xticks(x, languages)
    plt.legend()

    plt.savefig(f"results.png", dpi=300)


# Test the model for the files saved in tests.txt
def test():
    with open("tests.txt", "r") as tests:
        total_files = 0
        correct_outputs = 0
        cpp_found = java_found = rust_found = 0
        cpp_total = java_total = rust_total = 0

        # for each path and extension in tests.txt
        for line in tests.readlines():
            total_files += 1
            path, ext = line.split()
            if ext == "cpp":
                cpp_total += 1
            elif ext == "java":
                java_total += 1
            else:
                rust_total += 1

            try:
                # classify the file at the given path
                with open(path, "r") as file:
                    result = classify(file.read())
                    if result == ext:
                        correct_outputs += 1
                    if result == "cpp":
                        cpp_found += 1
                    elif result == "java":
                        java_found += 1
                    else:
                        rust_found += 1
            except (IOError, OSError, UnicodeDecodeError) as e:
                print(f"Failed to open: {path}")
                continue

    draw_results_graph([cpp_found, java_found, rust_found], [cpp_total, java_total, rust_total])
    return correct_outputs * 100 / total_files


# Test the model
accuracy = test()
print(f"Accuracy: {accuracy}\n")

'''# Separate input
new_input = "if else while"
classification = classify(new_input)
print(f"Input: '{new_input}' is classified as: {classification}")'''

training_files = {ext: open("training/training_" + ext + ".txt", 'w') for ext in ["cpp", "java", "rs"]}

index = 0
#Filling the training files
for word in selected_words:
        backslash_n = "\n"
        # If it's last keyword we don't print '\n
        if index == len(selected_words) - 1:
            backslash_n = ""

        training_files["cpp"].write("P(" + str(word) + "|cpp): " + str(keyword_probabilities_cpp[word]) + backslash_n)
        training_files["java"].write("P(" + str(word) + "|java): " + str(keyword_probabilities_java[word]) + backslash_n)
        training_files["rs"].write("P(" + str(word) + "|rs): " + str(keyword_probabilities_rust[word]) + backslash_n)

        index += 1

# Print the calculated probabilities for each keyword
# print("\nWord Probabilities:")
# for word in selected_words:
#     print(f"{word} - P(word|cpp): {keyword_probabilities_cpp[word]}, "
#           f"P(word|java): {keyword_probabilities_java[word]}, "
#           f"P(word|rust): {keyword_probabilities_rust[word]}")
