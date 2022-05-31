from PyQt5.QtWidgets import QMainWindow, QApplication, QTextEdit, QLineEdit, QLabel
from PyQt5 import uic
from PyQt5 import QtCore
from PyQt5 import Qt
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

        self.ok_not_ok = self.findChild(QLabel, "ok_not_ok")  # TESTING

        self.sequence_generation_source = constants.test_hiragana
        self.sequence_dictionary = constants.romaji_dict

        self.charStr = main.generate_sequence(15, self.sequence_generation_source)
        self.refreshOutput()

        self.show()

    def refreshOutput(self):
        self.outputBox.setText(self.charStr[:5])
        pass

    def getCurrentChar(self):
        return_char = self.charStr[0]
        if len(self.charStr) < 10:
            self.charStr += main.generate_sequence(10, self.sequence_generation_source)
        self.charStr = self.charStr[1:]
        self.refreshOutput()

        return return_char

    def EnterPress(self):
        inputted_letter = self.inputBox.text()
        correct_letter = self.getCurrentChar()

        self.ok_not_ok.setText(
            str(main.check_letter(inputted_letter, correct_letter, self.sequence_dictionary)))  # TESTING

        self.inputBox.setText("")
        pass


app = QApplication(sys.argv)
MainWindow = GUI()
app.exec_()

# TODO: disable scrolling on the output box
#  make text centered in the output box
#  make the main character the one in the middle, and not the one in the left
#  make the main character bigger
#  make passed characters red if they are failed and green if they are successful
#  clean up the file of unnecessary imports, test statements, etc
#  rewrite the file structure

# TODO big ideas:
#  make menus with options of choosing the hiragana to be displayed
#  integrate katakana
#  integrate kanji (???)