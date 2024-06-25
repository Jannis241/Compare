import os

currentDir = os.path.dirname(os.path.abspath(__file__))
frageCount = 1

class Word():
    def __init__(self, word) -> None:
        self.content = word
        self.betterWords = []
        self.worseWords = []
        self.rank = 0

    def isCombAlreadyEvaluated(self, otherWord):
        return otherWord in self.worseWords or otherWord in self.betterWords
    
    def getRank(self):
        return len(self.betterWords)

def getWords():
    words = []
    
    inputsPath = os.path.join(currentDir, 'inputs.txt')
    
    with open(inputsPath, 'r', encoding='utf-8') as file:
        for line in file:
            wort = line.strip()
            if wort:
                words.append(wort)
    return words

def askPreference(word1, word2):
    while True:
        print(f"Frage {frageCount}")
        print(f"(A) {word1.content}")
        print(f"(B) {word2.content}")
        choice = input(f"Wahl: ").lower()
        print("")
        if choice == "a":
            return word1
        elif choice == "b":
            return word2
        else:
            print("Ungültige Eingabe. Bitte wählen Sie 'A' oder 'B'.")  
                  
def writeOutput(sortedSelection):
    outputPath = os.path.join(currentDir, 'outputs.txt')
    if not os.path.exists(outputPath):
        open(outputPath, 'w').close()  # Erstelle die Datei, falls sie nicht existiert
    with open(outputPath, 'w', encoding='utf-8') as file:
        file.write("Das hier ist das Ranking basierend auf deinen Antworten!" + '\n')
        file.write('\n')
        for word in sortedSelection:
            file.write(word + '\n')

selection = getWords()

wordList = []

possibleCombinations = []

for w in selection:
    word = Word(w)
    wordList.append(word)

for word1 in wordList:
    for word2 in wordList: 

        if [word1, word2] in possibleCombinations:
            break
        
        if [word2, word1] in possibleCombinations:
            break
        
        if wordList.index(word1) == wordList.index(word2):
            break

        possibleCombinations.append([word1, word2])

print(f"Du musst jetzt {len(possibleCombinations)} Fragen beantworten")
print(f"Die Anzahl der Fragen wurde  von {len(selection) ** 2} zu {len(possibleCombinations)} optimiert.")
print()

sorted = False
for comb in possibleCombinations:
    word1 = comb[0]
    word2 = comb[1]

    if not word1.isCombAlreadyEvaluated(word2):
        choice = askPreference(word1, word2)
        frageCount += 1
        if choice == word1:
            word1.worseWords.append(word2)
            word2.betterWords.append(word1)
        if choice == word2:
            word2.worseWords.append(word1)
            word1.betterWords.append(word2)

rankMap = {}  # rank : word

for word in wordList:
    rank = word.getRank()
    if rank not in rankMap:
        rankMap[rank] = []
    rankMap[rank].append(word.content)

rankList = []
for rank in range(len(wordList)):
    if rank in rankMap:
        for word in rankMap[rank]:
            rankList.append(f"{rank + 1}. {word}")

writeOutput(rankList)