import io
import re
import pickle
from radix import SERadixTree


class SESpellChecker(SERadixTree):
    def __init__(self):
        # initialise our radix tree structure
        super().__init__()

        # compile our word cleaning pattern
        self.cleanPattern = re.compile("[^A-Za-z]")
        # compile our word search pattern
        self.wordPattern = re.compile("(\w+'\w+|\w+|\n)")

    def checkWord(self, word):
        # empty words are ignored
        if word == ' ' or word == '':
            return True

        # handle default SERadixTree word search
        return super().checkWord(word)

    def loadDictionary(self, dictionaryFile):
        # load our file
        with io.open(dictionaryFile, "r", encoding="utf-8") as dictFile:
            # load words into our Trie structure
            for word in dictFile.read().lower().split('\n'):
                self.addWord(word)
            # close our file
            dictFile.close()

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
            olen = len(word)
            x = 0

            # clean our word
            word = self.cleanPattern.sub("", word)

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
                    misspellings.append({"start": c-x, "length": olen})

                # update our character position
                c += olen # including the space
            else:
                # newline character
                c += 1

        # return a list of misspelled words
        return misspellings

    def saveState(self, toFile):
        try:
            with io.open(toFile, "wb") as document:
                document.write(pickle.dumps(self.__dict__))
                document.close()
        except:
            print("There was an error saving the spell checker's state to a file!")

    def restoreState(self, fromFile):
        try:
            with io.open(fromFile, "rb") as document:
                self.__dict__ = pickle.loads(document.read())
                document.close()
        except:
            print("There was an error restoring the spell checker's state from a file!")
