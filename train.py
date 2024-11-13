import numpy as np
import matplotlib.pyplot as plt

from typing import Tuple, Dict, List, Set

from probUtils import classify, getSelectedWords, getKeywordProbabilites

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

    plt.savefig(f"results/results.png", dpi=300)


# Test the model for the files saved in tests.txt
def test(selected_words):
    with open("resources/tests.txt", "r") as tests:
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
                    result = classify(file.read(), selected_words)
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

def fillTrainingFiles(selected_words):
    training_files = {ext: open("training/training_" + ext + ".txt", 'w') for ext in ["cpp", "java", "rs"]}
    keyword_probs_dist = getKeywordProbabilites(selected_words)

    index = 0
    #Filling the training files
    for word in selected_words:
            backslash_n = "\n"
            # If it's last keyword we don't print '\n
            if index == len(selected_words) - 1:
                backslash_n = ""
            
            for ext, keyword_prob in keyword_probs_dist.items():
                training_files[ext].write("P(" + str(word) + "|cpp): " + str(keyword_prob[word]) + backslash_n)
           
            index += 1
def main():
    # Test the model
    selected_words = getSelectedWords()
    accuracy = test(selected_words)
    print(f"Accuracy: {accuracy}\n")

    fillTrainingFiles(selected_words)

    '''# Separate input
    new_input = "if else while"
    classification = classify(new_input)
    print(f"Input: '{new_input}' is classified as: {classification}")'''

    
    

# Print the calculated probabilities for each keyword
# print("\nWord Probabilities:")
# for word in selected_words:
#     print(f"{word} - P(word|cpp): {keyword_probabilities_cpp[word]}, "
#           f"P(word|java): {keyword_probabilities_java[word]}, "
#           f"P(word|rust): {keyword_probabilities_rust[word]}")
