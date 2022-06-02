import random


def generate_sequence(length: int, sequence_list: tuple):
    sequence_list_len = len(sequence_list)

    sequence = []
    for i in range(0, length):
        rand_char = sequence_list[random.randint(0, sequence_list_len - 1)]
        #if len(rand_char) > 1:
        #    sequence.append((rand_char, True))
        #sequence.append((rand_char, False))
        sequence.append(rand_char)

    return sequence


def check_letter(inputted_letter: str, correct_letter: str, dc: dict):
    try:
        return correct_letter == dc[inputted_letter]
    except KeyError:
        return False