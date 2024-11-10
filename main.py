import numpy as np

import re
import math
from collections import defaultdict

# keywords selectate (cpp, rust, java)
selectedWords = " ".join(open("keywords.txt", "r").readlines()).split()

# numarul de aparitii keyword in fiecare categorie
cppKeyWords = defaultdict(int)
rustKeyWords = defaultdict(int)
javaKeyWords = defaultdict(int)

# numarul de cuvinte total in fiecare categorie:
# cppTotalWords, javaTotalWords, rustTotalWords

# cate file-uri am de fiecare categorie:
# dataCount, cppCount, javaCount, rustCount

cppResults = open("cpp_results.txt", "r")
cppTotalWords, cppCount = [int(n) for n in cppResults.readline().split()]
for line in cppResults.readlines():
    cppKeyWords[line.split()[0]] = int(line.split()[1])
cppResults.close()

javaResults = open("java_results.txt", "r")
javaTotalWords, javaCount = [int(n) for n in javaResults.readline().split()]
for line in javaResults.readlines():
    javaKeyWords[line.split()[0]] = int(line.split()[1])
javaResults.close()

rustResults = open("rs_results.txt", "r")
rustTotalWords, rustCount = [int(n) for n in rustResults.readline().split()]
for line in rustResults.readlines():
    rustKeyWords[line.split()[0]] = int(line.split()[1])
rustResults.close()

dataCount = cppCount + javaCount + rustCount

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


# in caz ca nu sunt fisiere de un anumit tip, TotalWords = 1 pentru a preveni impartire la 0
probabilitiesCpp = calcProbabilities(cppKeyWords, max(cppTotalWords, 1))
probabilitiesJava = calcProbabilities(javaKeyWords, max(javaTotalWords, 1))
probabilitiesRust = calcProbabilities(rustKeyWords, max(rustTotalWords, 1))


# Classification function
def classify(data):
    dataWords = set(re.findall(r'\w+', data.lower()))

    cppProbability = math.log(pCpp) if pCpp else 0
    javaProbability = math.log(pJava) if pJava else 0
    rustProbability = math.log(pRust) if pRust else 0

    '''
    Log Probabilities:
    The conditional probabilities for each class given an attribute value are small.
    When they are multiplied together they result in very small values, 
    which can lead to floating point underflow. 
    A common fix for this is to add the log of the probabilities together
    '''

    for word in dataWords:
        if word in selectedWords:
            cppProbability += math.log(probabilitiesCpp[word]) if probabilitiesCpp[word] else 0
            javaProbability += math.log(probabilitiesJava[word]) if probabilitiesJava[word] else 0
            rustProbability += math.log(probabilitiesRust[word]) if probabilitiesRust[word] else 0

    # daca nu exista fisiere de un anumit tip probabilitatea finala asociata categoriei e 0
    cppProbability = math.exp(cppProbability) if pCpp else 0
    javaProbability = math.exp(javaProbability) if pJava else 0
    rustProbability = math.exp(rustProbability) if pRust else 0

    res = [cppProbability, javaProbability, rustProbability]
    print(cppProbability, javaProbability, rustProbability, sep="  ")

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
