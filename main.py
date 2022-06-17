from PyQt5.QtWidgets import QMainWindow, QApplication, QLineEdit, QLabel, QPushButton, QCheckBox, QPlainTextEdit, \
    QFileDialog
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

        # Gui items from the selection ui

        self.cb_hiragana = None
        self.cb_katakana = None
        self.info_label_ok = None
        self.custom_kana_pte = None

        # Default character map

        self.sequence_generation_source = constants.generate_all()

        # Global variables

        self.future_list = GeneratorFunctions.generate_sequence(15, self.sequence_generation_source)
        self.curr_char = GeneratorFunctions.generate_sequence(1, self.sequence_generation_source)[0]
        self.past_list = [(True, ""), (True, ""), (True, "")]
        self.total_attempts = 0
        self.successful_attempts = 0
        self.seconds_passed = 0
        self.previous_attempt = True
        self.custom_sequence = ""
        self.file_dialog = QFileDialog()

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
        self.output_box_past = []
        self.output_box_future = []
        for i in range(1, 4):
            self.output_box_past.append(
                self.findChild(QLabel, "display_label_past_" + str(i))
            )
            self.output_box_future.append(
                self.findChild(QLabel, "display_label_future_" + str(i)),
            )
        self.input_box = self.findChild(QLineEdit, "input_box")
        self.success_rate_label = self.findChild(QLabel, "success_rate")
        self.kpm_label = self.findChild(QLabel, "kpm")
        self.correct_answer_label = self.findChild(QLabel, "correct_answer")

        refresh_btn = self.findChild(QPushButton, "btn_reset")
        go_to_select_btn = self.findChild(QPushButton, "btn_go_to_selection")

        refresh_btn.clicked.connect(self.refresh)
        go_to_select_btn.clicked.connect(self.load_selection_ui)
        self.input_box.returnPressed.connect(self.enter_press)

        self.refresh()

    def load_selection_ui(self):
        self.timer_thread.stop()
        uic.loadUi("selection_gui.ui", self)

        reset_selection_btn = self.findChild(QPushButton, "btn_selection_reset")
        go_to_main_btn = self.findChild(QPushButton, "btn_go_to_main")
        save_button = self.findChild(QPushButton, "btn_save_kana")
        load_button = self.findChild(QPushButton, "btn_load_kana")
        hiragana_select_all_btn = self.findChild(QPushButton, "btn_hiragana_select_all")
        katakana_select_all_btn = self.findChild(QPushButton, "btn_katakana_select_all")
        self.custom_kana_pte = self.findChild(QPlainTextEdit, "pte_custom_kana")
        self.info_label_ok = self.findChild(QLabel, "info_label_ok")

        self.cb_hiragana = []
        self.cb_katakana = []
        for cat in constants.constants["categories"]:
            self.cb_hiragana.append(
                {
                    "object": self.findChild(QCheckBox, "cb_hiragana_" + cat),
                    "cat": cat
                }
            )
            self.cb_katakana.append(
                {
                    "object": self.findChild(QCheckBox, "cb_katakana_" + cat),
                    "cat": cat
                }
            )

        go_to_main_btn.clicked.connect(self.to_main_ui)
        reset_selection_btn.clicked.connect(lambda: self.select_kana(self.cb_hiragana, False))
        reset_selection_btn.clicked.connect(lambda: self.select_kana(self.cb_katakana, False))
        hiragana_select_all_btn.clicked.connect(lambda: self.select_kana(self.cb_hiragana, True))
        katakana_select_all_btn.clicked.connect(lambda: self.select_kana(self.cb_katakana, True))
        save_button.clicked.connect(self.save_custom_to_file)
        load_button.clicked.connect(self.load_custom_from_file)
        self.custom_kana_pte.textChanged.connect(self.check_custom_sequence)

        self.custom_kana_pte.setPlainText(self.custom_sequence)

    def to_main_ui(self):
        self.sequence_generation_source = []
        for category_hiragana, category_katakana in zip(self.cb_hiragana, self.cb_katakana):
            if category_hiragana["object"].isChecked():
                self.sequence_generation_source += constants.constants["hiragana"][category_hiragana["cat"]]
            if category_katakana["object"].isChecked():
                self.sequence_generation_source += constants.constants["katakana"][category_katakana["cat"]]

        if self.check_custom_sequence():
            self.remember_custom_sequence()
            sequence = self.custom_sequence.split(',')
            for kana in sequence:
                if kana not in self.sequence_generation_source:
                    self.sequence_generation_source.append(kana)

        if len(self.sequence_generation_source) > 0:
            self.load_main_ui()

    def load_custom_from_file(self):
        file = QFileDialog.getOpenFileName(self, 'Open kana list', '', 'Kana text files (*.kana)')[0]
        if not file:
            return
        with open(file, 'r') as f:
            text = f.read()
        self.custom_kana_pte.setPlainText(text)

    def save_custom_to_file(self):
        if not self.check_custom_sequence():
            return
        file = QFileDialog.getSaveFileName(self, 'Save kana list', '', 'Kana text files (*.kana)')[0]
        if not file:
            return
        self.remember_custom_sequence()
        with open(file, 'w') as f:
            f.write(self.custom_sequence)

    def select_kana(self, cb_list: list, selected: bool):
        for category in cb_list:
            category["object"].setChecked(selected)

    def check_custom_sequence(self):
        if GeneratorFunctions.check_sequence(self.custom_kana_pte.toPlainText()):
            self.info_label_ok.setText("<font color=#00FF00>List OK!</font>")
            return True

        self.info_label_ok.setText("<font color=#FF0000>List not OK!</font>")
        return False

    def remember_custom_sequence(self):
        sequence = self.custom_kana_pte.toPlainText().split(',')
        self.custom_sequence = ""
        for kana in sequence:
            if kana == "":
                continue
            self.custom_sequence += kana + ","


app = QApplication(sys.argv)
MainWindow = GUI()
app.exec_()
