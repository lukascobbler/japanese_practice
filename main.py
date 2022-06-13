from PyQt5.QtWidgets import QMainWindow, QApplication, QLineEdit, QLabel, QPushButton, QCheckBox
from PyQt5 import uic
from PyQt5.QtCore import QTimer
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
        self.kpm_label = None
        self.correct_answer_label = None

        self.refresh_btn = None
        self.go_to_select_btn = None

        # Gui items from the selection ui

        self.reset_selection_btn = None
        self.go_to_main_btn = None
        self.hiragana_select_all_btn = None
        self.katakana_select_all_btn = None

        # Default character maps

        self.sequence_generation_source = constants.generate_all()
        # self.inverse_dictionary = constants.hiragana_romaji_dict
        # self.sequence_dictionary = constants.romaji_hiragana_dict

        # Global variables

        self.future_list = GeneratorFunctions.generate_sequence(15, self.sequence_generation_source)
        self.curr_char = GeneratorFunctions.generate_sequence(1, self.sequence_generation_source)[0]
        self.past_list = [(True, ""), (True, ""), (True, "")]
        self.total_attempts = 0
        self.successful_attempts = 0
        self.seconds_passed = 0
        self.previous_attempt = True
        self.cb_hiragana = []
        self.cb_katakana = []

        self.timer_thread = QTimer()
        self.timer_thread.timeout.connect(self.update_kpm)
        self.timer_thread.setInterval(750)

        self.load_main_ui()

        self.show()

    def refresh(self):
        self.future_list = GeneratorFunctions.generate_sequence(15, self.sequence_generation_source)
        self.curr_char = GeneratorFunctions.generate_sequence(1, self.sequence_generation_source)[0]
        self.past_list = [(True, ""), (True, ""), (True, "")]
        self.total_attempts = 0
        self.successful_attempts = 0
        self.seconds_passed = 0
        self.previous_attempt = True
        self.timer_thread.stop()
        self.update_kpm()
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
        self.correct_answer_label.setText(
            GeneratorFunctions.get_inverse_html(self.past_list[-1])
        )

    def update_kpm(self):
        self.seconds_passed += 0.75
        self.kpm_label.setText(
            GeneratorFunctions.get_kpm_html(self.total_attempts, self.seconds_passed)
        )

    def check_lengths(self):
        if len(self.future_list) < 10:
            self.future_list += GeneratorFunctions.generate_sequence(10, self.sequence_generation_source)

        if len(self.past_list) > 10:
            self.past_list = self.past_list[-10:]

    def enter_press(self):
        if not self.timer_thread.isActive():
            self.timer_thread.start()

        self.check_lengths()

        inputted_text = self.input_box.text().lower()
        correct_letter = self.curr_char

        success = GeneratorFunctions.check_letter(inputted_text, correct_letter)

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
        self.kpm_label = self.findChild(QLabel, "kpm")
        self.correct_answer_label = self.findChild(QLabel, "correct_answer")

        self.refresh_btn = self.findChild(QPushButton, "btn_reset")
        self.go_to_select_btn = self.findChild(QPushButton, "btn_go_to_selection")

        self.refresh_btn.clicked.connect(self.refresh)
        self.go_to_select_btn.clicked.connect(self.load_selection_ui)
        self.input_box.returnPressed.connect(self.enter_press)

        self.refresh()

    def to_main_ui(self):
        self.sequence_generation_source = []
        for category_hiragana, category_katakana in zip(self.cb_hiragana, self.cb_katakana):
            if category_hiragana["object"].isChecked():
                self.sequence_generation_source += category_hiragana["characters"]
            if category_katakana["object"].isChecked():
                self.sequence_generation_source += category_katakana["characters"]

        if len(self.sequence_generation_source) > 0:
            self.load_main_ui()

    def load_selection_ui(self):
        self.timer_thread.stop()
        uic.loadUi("selection_gui.ui", self)

        self.reset_selection_btn = self.findChild(QPushButton, "btn_selection_reset")
        self.go_to_main_btn = self.findChild(QPushButton, "btn_go_to_main")
        self.hiragana_select_all_btn = self.findChild(QPushButton, "btn_hiragana_select_all")
        self.katakana_select_all_btn = self.findChild(QPushButton, "btn_katakana_select_all")

        self.cb_hiragana = []
        self.cb_katakana = []
        for let in constants.constants["letters"]:
            self.cb_hiragana.append(
                {
                    "object": self.findChild(QCheckBox, "cb_hiragana_" + let),
                    "characters": constants.constants["hiragana"][let]
                }
            )
            self.cb_katakana.append(
                {
                    "object": self.findChild(QCheckBox, "cb_katakana_" + let),
                    "characters": constants.constants["katakana"][let]
                }
            )

        self.go_to_main_btn.clicked.connect(self.to_main_ui)
        self.reset_selection_btn.clicked.connect(lambda: self.select_kana(self.cb_hiragana, False))
        self.reset_selection_btn.clicked.connect(lambda: self.select_kana(self.cb_katakana, False))
        self.hiragana_select_all_btn.clicked.connect(lambda: self.select_kana(self.cb_hiragana, True))
        self.katakana_select_all_btn.clicked.connect(lambda: self.select_kana(self.cb_katakana, True))

    def select_kana(self, cb_list: list, selected: bool):
        for category in cb_list:
            category["object"].setChecked(selected)


app = QApplication(sys.argv)
MainWindow = GUI()
app.exec_()
