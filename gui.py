from PyQt5.QtWidgets import QMainWindow, QApplication, QTextEdit, QLineEdit
from PyQt5 import uic
from PyQt5 import QtCore
from PyQt5 import Qt
import sys

import main # TEMPORARY

class GUI(QMainWindow):
    def __init__(self):
        super(GUI, self).__init__()

        uic.loadUi("gui.ui", self)

        self.outputBox = self.findChild(QTextEdit, "output_box")
        self.inputBox = self.findChild(QLineEdit, "input_box")

        self.inputBox.returnPressed.connect(self.EnterPress)

        self.charList = main.generate_sequence(15)
        self.refreshOutput()

        self.show()

    def charListToOutput(self):
        char_str = ""
        for i in range(0, 6):
            char_str += self.charList[i]

        return char_str

    def refreshOutput(self):
        self.outputBox.setText(self.charListToOutput())
        pass

    def getCurrentChar(self):
        return_char = self.charList.pop(0)
        if len(self.charList) < 10:
            self.charList.extend(main.generate_sequence(10)) # REQUEST AN EXTENSTION HERE, FROM THE MAIN FILE
        self.refreshOutput()

        return return_char

    def EnterPress(self):
        # TODO:
        # MAKE THE NEXT CHARACTER DISPLAY
        # CHECK FOR ERRORS

        # self.inputBox.text() CHECK USING A DICTIONARY
        self.inputBox.setText("")
        pass


app = QApplication(sys.argv)
MainWindow = GUI()
app.exec_()

# general TODO: disable scrolling on the output box