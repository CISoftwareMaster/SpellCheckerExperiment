import os
import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.Qt import Qt, QApplication
from SESpellChecker import SESpellChecker


# data IDs
WordCursor = 1213
WordName = 1214


class SESpellcheckHighlighter(QSyntaxHighlighter):
    def __init__(self, doc):
        super().__init__(doc)

        # initialise our spell checker
        self.spellchecker = SESpellChecker()

        # misspelling style
        self.mispelledWord = QTextCharFormat()
        self.mispelledWord.setUnderlineColor(Qt.red)
        self.mispelledWord.setUnderlineStyle(QTextCharFormat.SingleUnderline)

        # load our English dictionary
        self.spellchecker.loadDictionary("dictionary.txt")
        # optimise our spellchecker's word tree
        self.spellchecker.optimise()

        print(f"Spellchecker Word Tree node count: {self.spellchecker.totalNodeCount():,}")

    def highlightBlock(self, text):
        # get misspellings
        for misspelling in self.spellchecker.spellCheck(text):
            # highlight misspelling
            self.setFormat(misspelling["start"], misspelling["length"], self.mispelledWord)

class TextEditor(QPlainTextEdit):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(640, 480)

        # set editor font
        font = self.font()
        font.setPointSize(18)
        self.setFont(font)

        # initialise our misspelling highlighter
        self.highlighter = SESpellcheckHighlighter(self.document())
        # get reference to our spellchecker
        self.spellchecker = self.highlighter.spellchecker

if __name__ == "__main__":
    app = QApplication(sys.argv)
    textEditor = TextEditor()
    textEditor.show()
    sys.exit(app.exec_())
