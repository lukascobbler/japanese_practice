import random


def generate_sequence(length: int, sequence_list: tuple):
    sequence_list_len = len(sequence_list)

    sequence = []
    for i in range(0, length):
        rand_char = sequence_list[random.randint(0, sequence_list_len - 1)]
        sequence.append(rand_char)

    return sequence


def check_letter(inputted_letter: str, correct_letter: str, dc: dict):
    try:
        return correct_letter == dc[inputted_letter]
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
