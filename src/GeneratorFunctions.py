import random

import constants


def generate_sequence(length: int, sequence_list: tuple):
    sequence_list_len = len(sequence_list)

    sequence = []
    for i in range(0, length):
        rand_char = sequence_list[random.randint(0, sequence_list_len - 1)]
        sequence.append(rand_char)

    return sequence


def check_letter(inputted_letter: str, correct_letter: str):
    try:
        return correct_letter == constants.hiragana_direct_dict[inputted_letter] or \
               correct_letter == constants.katakana_direct_dict[inputted_letter]
    except KeyError:
        return False


def get_past_html(past_list: list):
    html = []
    for success, correct_char in past_list[-3:]:
        if success:
            html.append("<font color=#00FF00 size=1>" + correct_char + "</font>")
        else:
            html.append("<font color=#FF0000 size=1>" + correct_char + "</font>")

    return html


def get_current_html(curr_char: str):
    return "<font color=#000000 size=4>" + curr_char + "</font>"


def get_future_html(future_list: list):
    html = []
    for letter in future_list[:5]:
        html.append("<font color=#000000 size=1>" + letter + "</font>")
    return html


def get_success_html(total_attempts: int, successful_attempts: int, previous_attempt: bool):
    if total_attempts == 0:
        return "<font color=#00FF00>0%</font>"

    success_rate = round(successful_attempts / total_attempts * 100)
    if previous_attempt:
        return "<font color=#00FF00>" + str(success_rate) + "%</font>"
    else:
        return "<font color=#FF0000>" + str(success_rate) + "%</font>"


def get_kpm_html(total_attempts: int, seconds_passed: int):
    minutes_passed = seconds_passed / 60
    kpm = round(total_attempts / minutes_passed, 1)
    if kpm > 999:
        kpm = 999.0

    if kpm > 20:
        return "<font color=#00FF00>" + str(kpm) + "</font>"
    else:
        return "<font color=#FF0000>" + str(kpm) + "</font>"


def get_inverse_html(previous_attempt: tuple):
    success, previous_char = previous_attempt
    try:
        inverse_char = katakana_or_hiragana_inverse(previous_char)[previous_char]
    except KeyError:
        inverse_char = ''
    if success:
        return "<font color=#00FF00>" + inverse_char + "</font>"
    else:
        return "<font color=#FF0000>" + inverse_char + "</font>"


def katakana_or_hiragana_inverse(char: str):
    if char in constants.constants["hiragana"]["_all"]:
        return constants.hiragana_inverse_dict
    elif char in constants.constants["katakana"]["_all"]:
        return constants.katakana_inverse_dict
    return {}


def check_sequence(sequence: str):
    for kana in sequence.split(","):
        if kana == "":
            continue
        if kana not in constants.constants["hiragana"]["_all"] and kana not in constants.constants["katakana"]["_all"]:
            return False
    return True
