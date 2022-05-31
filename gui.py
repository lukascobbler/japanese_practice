from PyQt5.QtWidgets import QMainWindow, QApplication, QTextEdit, QLineEdit
from PyQt5 import uic
from PyQt5.QtCore import Qt
import sys

import constants
import main  # TEMPORARY


class GUI(QMainWindow):
    def __init__(self):
        super(GUI, self).__init__()

        uic.loadUi("gui.ui", self)

        self.outputBox = self.findChild(QTextEdit, "output_box")
        self.inputBox = self.findChild(QLineEdit, "input_box")

        self.inputBox.returnPressed.connect(self.EnterPress)

        self.sequence_generation_source = constants.test_hiragana
        self.sequence_dictionary = constants.romaji_dict

        self.futureStr = main.generate_sequence(15, self.sequence_generation_source)
        self.currChar = main.generate_sequence(1, self.sequence_generation_source)
        self.pastAttempts = []

        self.refreshOutput()

        self.show()

    def refreshOutput(self):
        self.outputBox.setHtml(
            self.getPastHtml() +
            self.getCurrentHtml() +
            self.getFutureHtml()
        )
        self.outputBox.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)


    def checkLengths(self):
        if len(self.futureStr) < 10:
            self.futureStr += main.generate_sequence(10, self.sequence_generation_source)

        if len(self.pastAttempts) > 10:
            self.pastAttempts = self.pastAttempts[-10:]


    def getPastHtml(self):
        html = ""
        for success, correct_char in self.pastAttempts[-4:]:
            if success:
                html += "<font color=#00FF00 size=1>" + correct_char + "</font>"
            else:
                html += "<font color=#FF0000 size=1>" + correct_char + "</font>"

        return html


    def getCurrentHtml(self):
        return "<font color=#000000 size=4>" + self.currChar + "</font>"


    def getFutureHtml(self):
        html = ""
        for letter in self.futureStr[:4]:
            html += "<font color=#000000 size=1>" + letter + "</font>"
        return html


    def EnterPress(self):
        self.checkLengths()

        inputted_text = self.inputBox.text()
        correct_letter = self.currChar

        success = main.check_letter(inputted_text, correct_letter, self.sequence_dictionary)

        if success:
            self.pastAttempts.append((True, correct_letter))
        else:
            self.pastAttempts.append((False, correct_letter))

        self.currChar = self.futureStr[0]
        self.futureStr = self.futureStr[1:]

        self.refreshOutput()

        self.inputBox.setText("")


app = QApplication(sys.argv)
MainWindow = GUI()
app.exec_()

# TODO: disable scrolling on the output box
#  clean up the file of unnecessary imports, test statements, etc
#  rewrite the file structure

# TODO big ideas:
#  make menus with options of choosing the hiragana to be displayed
#  integrate katakana
#  integrate kanji (???)