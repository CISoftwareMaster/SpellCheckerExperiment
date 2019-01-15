import io
import re


class SETrieNode:
    def __init__(self):
        self.isWord = False
        # create 27 children for this node
        self.children = [None for _ in range(27)]


class SESpellChecker:
    def __init__(self):
        # initialise our (27) base Trie nodes
        self.children = [SETrieNode() for _ in range(27)]
        self.wordPattern = re.compile("(\w+'\w+|\w+|\n)")

    def loadDictionary(self, dictionaryFile):
        # load our file
        with io.open(dictionaryFile, "r", encoding="utf-8") as dictFile:
            # load words into our Trie structure
            for word in dictFile.read().lower().split('\n'):
                self.addWord(word)
            # close our file
            dictFile.close()

    def addWord(self, word):
        indexes = [j for j in [self.mapToIndex(i) for i in word] if j is not None]

        # check if we got a valid index list
        if len(indexes) > 0:
            # pointer is set to one of our base Trie node
            pointer = self.children[indexes[0]]

            # create / follow branches until we reach the last node
            for i in range(1, len(indexes)):
                if pointer.children[indexes[i]] is None:
                    pointer.children[indexes[i]] = SETrieNode()
                pointer = pointer.children[indexes[i]]

            # mark it as a word
            pointer.isWord = True

    def checkWord(self, word):
        indexes = [j for j in [self.mapToIndex(i) for i in word] if j is not None]

        # if it's a hyphen, ignore it
        if word == '-':
            return True

        # check if we have a valid pathway
        if len(indexes) > 0:
            pointer = self.children[indexes[0]]

            # follow branches until we reach the last node
            for i in range(1, len(indexes)):
                if pointer.children[indexes[i]] is not None:
                    pointer = pointer.children[indexes[i]]
                else:
                    # it's not a word
                    return False

            # we found the leaf! Check its value
            return pointer.isWord

        # nothing to correct here
        return True

    def mapToIndex(self, char):
        # make sure we're working on lowercase characters
        char = char.lower()

        # map it to an index value
        if char == "'":
            return 26
        elif ord(char) >= ord('a') and ord(char) <= ord('z'):
            return ord('z') - ord(char)

    def spellCheck(self, doc):
        # list of misspelled words
        misspellings = []
        # current character
        c = 0
        # extract words from our document
        words = self.wordPattern.split(doc)

        # iterate through every word
        for i in range(len(words)):
            word = words[i]
            x = 0

            if word != '\n':
                # words that end in 's
                if word.endswith("'s"):
                    word = word.strip("'s")

                    # start 2 characters earlier later
                    x = 2

                    # but still add those characters in our position counter
                    c = c + 2

                # check if this word doesn't match
                if not self.checkWord(word):
                    misspellings.append({"start": c-x, "length": len(word)})

                # update our character position
                c += len(word) # including the space
            else:
                c += 1

        # return a list of misspelled words
        return misspellings
