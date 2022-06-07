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

        self.output_box_current = self.findChild(QLabel, "display_label_current")
        self.output_box_past = [
            self.findChild(QLabel, "display_label_past_1"),
            self.findChild(QLabel, "display_label_past_2"),
            self.findChild(QLabel, "display_label_past_3"),
        ]
        self.output_box_future = [
            self.findChild(QLabel, "display_label_future_1"),
            self.findChild(QLabel, "display_label_future_2"),
            self.findChild(QLabel, "display_label_future_3"),
        ]
        self.input_box = self.findChild(QLineEdit, "input_box")
        self.success_rate_label = self.findChild(QLabel, "success_rate")

        self.refresh_btn = self.findChild(QPushButton, "btn_reset")
        self.refresh_btn.clicked.connect(self.refresh)

        self.input_box.returnPressed.connect(self.enter_press)

        self.sequence_generation_source = constants.katakana
        self.sequence_dictionary = constants.romaji_katakana_dict

        self.future_list = GeneratorFunctions.generate_sequence(15, self.sequence_generation_source)
        self.curr_char = GeneratorFunctions.generate_sequence(1, self.sequence_generation_source)[0]
        self.past_list = [(True, ""), (True, ""), (True, "")]
        self.total_attempts = 0
        self.successful_attempts = 0
        self.previous_attempt = True

        self.refresh_output()

        self.show()

    def refresh(self):
        self.future_list = GeneratorFunctions.generate_sequence(15, self.sequence_generation_source)
        self.curr_char = GeneratorFunctions.generate_sequence(1, self.sequence_generation_source)[0]
        self.past_list = [(True, ""), (True, ""), (True, "")]
        self.total_attempts = 0
        self.successful_attempts = 0
        self.previous_attempt = True
        self.refresh_output()

    def refresh_output(self):
        self.output_box_current.setText(
            self.get_current_html()
        )
        future_html = self.get_future_html()
        past_html = self.get_past_html()

        for f_html, f_box in zip(future_html, self.output_box_future):
            f_box.setText(f_html)

        for p_html, p_box in zip(past_html, reversed(self.output_box_past)):
            try:
                p_box.setText(p_html)
            except IndexError:
                pass

        self.success_rate_label.setText(self.get_success_html())
        self.success_rate_label.setAlignment(Qt.AlignRight)

    def check_lengths(self):
        if len(self.future_list) < 10:
            self.future_list += GeneratorFunctions.generate_sequence(10, self.sequence_generation_source)

        if len(self.past_list) > 10:
            self.past_list = self.past_list[-10:]

    def get_past_html(self):
        html = []
        for success, correct_char in self.past_list[-3:]:
            if success:
                html.append("<font color=#00FF00 size=1>" + correct_char + "</font>")
            else:
                html.append("<font color=#FF0000 size=1>" + correct_char + "</font>")

        return html

    def get_current_html(self):
        return "<font color=#000000 size=4>" + self.curr_char + "</font>"

    def get_future_html(self):
        html = []
        for letter in self.future_list[:5]:
            html.append("<font color=#000000 size=1>" + letter + "</font>")
        return html

    def get_success_html(self):
        if self.total_attempts == 0:
            return "<font color=#00FF00>100%</font>"

        success_rate = round(self.successful_attempts / self.total_attempts * 100)
        if self.previous_attempt:
            return "<font color=#00FF00>" + str(success_rate) + "%</font>"
        else:
            return "<font color=#FF0000>" + str(success_rate) + "%</font>"

    def enter_press(self):
        self.check_lengths()

        inputted_text = self.input_box.text()
        correct_letter = self.curr_char

        success = GeneratorFunctions.check_letter(inputted_text, correct_letter, self.sequence_dictionary)

        if success:
            self.past_list.append((True, correct_letter))
            self.successful_attempts += 1
            self.previous_attempt = True
        else:
            self.past_list.append((False, correct_letter))
            self.previous_attempt = False

        self.total_attempts += 1

        self.curr_char = self.future_list[0]
        self.future_list = self.future_list[1:]

        self.refresh_output()

        self.input_box.setText("")


app = QApplication(sys.argv)
MainWindow = GUI()
app.exec_()
