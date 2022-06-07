from PyQt5.QtWidgets import QMainWindow, QApplication, QLineEdit, QLabel, QPushButton
from PyQt5 import uic
from PyQt5.QtCore import Qt
import sys
import constants
import GeneratorFunctions


class GUI(QMainWindow):
    def __init__(self):
        super(GUI, self).__init__()

        # Gui items from the main ui

        self.output_box_current = None
        self.output_box_past = None
        self.output_box_future = None
        self.input_box = None
        self.success_rate_label = None

        self.refresh_btn = None
        self.go_to_select_btn = None

        # Gui items from the selection ui

        self.reset_selection_btn = None
        self.go_to_main_btn = None
        self.hiragana_select_all_btn = None
        self.katakana_select_all_btn = None

        # Default character maps

        self.sequence_generation_source = constants.hiragana
        self.sequence_dictionary = constants.romaji_hiragana_dict

        # Global variables

        self.future_list = GeneratorFunctions.generate_sequence(15, self.sequence_generation_source)
        self.curr_char = GeneratorFunctions.generate_sequence(1, self.sequence_generation_source)[0]
        self.past_list = [(True, ""), (True, ""), (True, "")]
        self.total_attempts = 0
        self.successful_attempts = 0
        self.previous_attempt = True

        self.load_main_ui()

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
        self.output_box_current.setText(GeneratorFunctions.get_current_html(self.curr_char))
        future_html = GeneratorFunctions.get_future_html(self.future_list)
        past_html = GeneratorFunctions.get_past_html(self.past_list)

        for f_html, f_box in zip(future_html, self.output_box_future):
            f_box.setText(f_html)

        for p_html, p_box in zip(past_html, reversed(self.output_box_past)):
            try:
                p_box.setText(p_html)
            except IndexError:
                pass

        self.success_rate_label.setText(
            GeneratorFunctions.get_success_html(self.total_attempts, self.successful_attempts, self.previous_attempt)
        )
        self.success_rate_label.setAlignment(Qt.AlignRight)

    def check_lengths(self):
        if len(self.future_list) < 10:
            self.future_list += GeneratorFunctions.generate_sequence(10, self.sequence_generation_source)

        if len(self.past_list) > 10:
            self.past_list = self.past_list[-10:]

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

    def load_main_ui(self):
        uic.loadUi("main_gui.ui", self)
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
        self.go_to_select_btn = self.findChild(QPushButton, "btn_go_to_selection")

        self.refresh_btn.clicked.connect(self.refresh)
        self.go_to_select_btn.clicked.connect(self.load_selection_ui)
        self.input_box.returnPressed.connect(self.enter_press)

        self.refresh()

    def load_selection_ui(self):
        uic.loadUi("selection_gui.ui", self)

        self.reset_selection_btn = self.findChild(QPushButton, "btn_selection_reset")
        self.go_to_main_btn = self.findChild(QPushButton, "btn_go_to_main")
        self.hiragana_select_all_btn = self.findChild(QPushButton, "btn_hiragana_select_all")
        self.katakana_select_all_btn = self.findChild(QPushButton, "btn_katakana_select_all")

        self.go_to_main_btn.clicked.connect(self.load_main_ui)
        self.hiragana_select_all_btn.clicked.connect(self.select_all_hiragana)
        self.katakana_select_all_btn.clicked.connect(self.select_all_katakana)

    def select_all_hiragana(self):
        self.sequence_generation_source = constants.hiragana
        self.sequence_dictionary = constants.romaji_hiragana_dict

    def select_all_katakana(self):
        self.sequence_generation_source = constants.katakana
        self.sequence_dictionary = constants.romaji_katakana_dict


app = QApplication(sys.argv)
MainWindow = GUI()
app.exec_()
