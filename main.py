from typing import Tuple, Dict, List, Set
from probUtils import classify, getSelectedWords

def main():
    input_file = open("input.txt", "r")
    data = input_file.read()
    selected_words = getSelectedWords()
    print(f"Input.txt is actually .{classify(data, selected_words)} file!")

main()