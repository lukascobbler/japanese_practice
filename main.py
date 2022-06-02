from PyQt5.QtWidgets import QMainWindow, QApplication, QLineEdit, QLabel, QPushButton
from PyQt5 import uic
from PyQt5.QtCore import Qt
import sys
import constants
import GeneratorFunctions


class GUI(QMainWindow):
    def __init__(self):
        super(GUI, self).__init__()

        uic.loadUi("gui.ui", self)

        self.outputBoxCurrent = self.findChild(QLabel, "display_label_current")
        self.outputBoxPast = self.findChild(QLabel, "display_label_past")
        self.outputBoxFuture = self.findChild(QLabel, "display_label_future")
        self.inputBox = self.findChild(QLineEdit, "input_box")
        self.success_rate_label = self.findChild(QLabel, "success_rate")

        self.refresh_btn = self.findChild(QPushButton, "btn_reset")
        self.refresh_btn.clicked.connect(self.refresh)

        self.inputBox.returnPressed.connect(self.EnterPress)

        self.sequence_generation_source = constants.hiragana
        self.sequence_dictionary = constants.romaji_dict

        self.refresh()
        self.show()


    def refresh(self):
        self.futureList = GeneratorFunctions.generate_sequence(15, self.sequence_generation_source)
        self.currChar = GeneratorFunctions.generate_sequence(1, self.sequence_generation_source)[0]
        self.pastList = []
        self.total_attempts = 0
        self.successful_attempts = 0
        self.previous_attempt = True
        self.refreshOutput()


    def refreshOutput(self):
        self.outputBoxCurrent.setText(
            self.getCurrentHtml()
        )
        self.outputBoxPast.setText(
            self.getPastHtml()
        )
        self.outputBoxFuture.setText(
            self.getFutureHtml()
        )
        self.success_rate_label.setText(self.getSucessHtml())
        # self.outputBox.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        self.success_rate_label.setAlignment(Qt.AlignRight)


    def checkLengths(self):
        if len(self.futureList) < 10:
            self.futureList += GeneratorFunctions.generate_sequence(10, self.sequence_generation_source)

        if len(self.pastList) > 10:
            self.pastList = self.pastList[-10:]


    def getPastHtml(self):
        html = ""
        for success, correct_char in self.pastList[-5:]:
            if success:
                html += "<font color=#00FF00 size=1>" + correct_char + "</font>"
            else:
                html += "<font color=#FF0000 size=1>" + correct_char + "</font>"

        return html


    def getCurrentHtml(self):
        return "<font color=#000000 size=4>" + self.currChar + "</font>"


    def getFutureHtml(self):
        html = ""
        for letter in self.futureList[:5]:
            html += "<font color=#000000 size=1>" + letter + "</font>"
        return html

    def getSucessHtml(self):
        if self.total_attempts == 0:
            return "<font color=#00FF00>100%</font>"

        success_rate = round(self.successful_attempts / self.total_attempts * 100)
        if self.previous_attempt:
            return "<font color=#00FF00>" + str(success_rate) + "%</font>"
        else:
            return "<font color=#FF0000>" + str(success_rate) + "%</font>"

    def EnterPress(self):
        self.checkLengths()

        inputted_text = self.inputBox.text()
        correct_letter = self.currChar

        success = GeneratorFunctions.check_letter(inputted_text, correct_letter, self.sequence_dictionary)

        if success:
            self.pastList.append((True, correct_letter))
            self.successful_attempts += 1
            self.previous_attempt = True
        else:
            self.pastList.append((False, correct_letter))
            self.previous_attempt = False

        self.total_attempts += 1

        self.currChar = self.futureList[0]
        self.futureList = self.futureList[1:]

        self.refreshOutput()

        self.inputBox.setText("")


app = QApplication(sys.argv)
MainWindow = GUI()
app.exec_()

# TODO: disable scrolling on the output box
#  add wpm
#  fix double hiragana bug

# TODO big ideas:
#  make menus with options of choosing the hiragana to be displayed
#  integrate katakana
#  integrate kanji (???)
