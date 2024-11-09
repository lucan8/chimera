import numpy as np

import re
from collections import defaultdict

dataset = [
    ("if public class", "Java"),
    ("for void int", "Java"),
    ("while public double", "Java"),
    ("class public void", "Java"),
    ("if else public", "Java"),
    ("let mut fn", "Rust"),
    ("for while match", "Rust"),
    ("if let mut", "Rust"),
    ("while let fn", "Rust"),
    ("mut match for", "Rust"),
    ("for void include", "C++"),
    ("if include int", "C++"),
    ("else public include", "C++"),
    ("class include public", "C++"),
    ("for while include", "C++"),
    ("while void public", "C++"),
    ("include public int", "C++"),
    ("if class public", "C++"),
    ("let mut while", "Rust"),
    ("if else while", "Java")
]

# keywords selectate (cpp, rust, java)
selectedWords = {"if", "else", "for", "while", "let", "mut", "class", "public", "void", "include"}

# numarul de aparitii keyword in fiecare categorie
cppKeyWords = defaultdict(int)
rustKeyWords = defaultdict(int)
javaKeyWords = defaultdict(int)

# numarul de cuvinte total in fiecare categorie
cppTotalWords = 0
rustTotalWords = 0
javaTotalWords = 0

# numar de cate ori apare fiecare cuvant in fiecare categorie
for data, label in dataset:
    # toate cuvintele din data
    words = set(re.findall(r'\w+', data.lower()))
    for word in words:
        if label == "C++":
            cppTotalWords += 1
            if word in selectedWords:
                cppKeyWords[word] += 1
        elif label == "Java":
            javaTotalWords += 1
            if word in selectedWords:
                javaKeyWords[word] += 1
        else:
            rustTotalWords += 1
            if word in selectedWords:
                rustKeyWords[word] += 1

# cate inputuri am de fiecare tip
dataCount = len(dataset)
cppCount = sum(1 for t in dataset if t[1] == "C++")
javaCount = sum(1 for t in dataset if t[1] == "Java")
rustCount = sum(1 for t in dataset if t[1] == "Rust")

# probabilitati a priori
pCpp = cppCount / dataCount
pJava = javaCount / dataCount
pRust = rustCount / dataCount


# calculez probabilitatile conditionate pentru fiecare categorie
# smoothing e additive/Laplace smoothing
def calcProbabilities(wordDict, totalWords, smoothing=0):
    probabilities = dict()
    for keyword in selectedWords:
        probabilities[keyword] = (wordDict.get(keyword, 0) + smoothing) \
            / (totalWords + smoothing * len(selectedWords))
    return probabilities


probabilitiesCpp = calcProbabilities(cppKeyWords, cppTotalWords)
probabilitiesJava = calcProbabilities(javaKeyWords, javaTotalWords)
probabilitiesRust = calcProbabilities(rustKeyWords, rustTotalWords)


# Classification function
def classify(data):
    dataWords = set(re.findall(r'\w+', data.lower()))

    cppProbability = pCpp
    javaProbability = pJava
    rustProbability = pRust

    for word in dataWords:
        if word in selectedWords:
            cppProbability *= probabilitiesCpp[word]
            javaProbability *= probabilitiesJava[word]
            rustProbability *= probabilitiesRust[word]

    res = [cppProbability, javaProbability, rustProbability]
    if max(res) == cppProbability:
        return "C++"
    elif max(res) == javaProbability:
        return "Java"
    else:
        return "Rust"

# testez
newInput = "if else while"
classification = classify(newInput)
print(f"Input: '{newInput}' is classified as: {classification}")

# probabilitati
print("\nWord Probabilities:")
for word in selectedWords:
    print(f"{word} - P(word|cpp): {probabilitiesCpp[word]}, "
          f"P(word|java): {probabilitiesJava[word]}, "
          f"P(word|rust): {probabilitiesRust[word]}")
