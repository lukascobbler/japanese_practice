import random
import colorama
import constants

test_hiragana = ('あ', 'い', 'う', 'え', 'お', 'か', 'き', 'く', 'け', 'こ')


def generate_sequence(length: int, sequence_list: tuple = None):
    if sequence_list is None:
        sequence_list = constants.hiragana
    sequence_list_len = len(sequence_list)

    sequence = []
    for i in range(0, length):
        rand_char = sequence_list[random.randint(0, sequence_list_len - 1)]
        sequence.append(rand_char)

    return sequence


def check_inputted_sequence(inputted_sequence: list, given_sequence: list, dict: dict=None):
    if dict is None:
        dict = constants.romaji_dict

    failed_guesses = ""

    for inp_word, giv_word in zip(inputted_sequence, given_sequence):
        try:
            if dict[inp_word] != giv_word:
                failed_guesses += colorama.Fore.RED + inp_word + " " + colorama.Fore.RESET
                continue
        except KeyError:
            failed_guesses += colorama.Fore.RED + inp_word + " " + colorama.Fore.RESET
            continue
        failed_guesses += colorama.Fore.GREEN + inp_word + " " + colorama.Fore.RESET

    return failed_guesses

l = int(input('Enter the length\n'))
while True:
    colorama.init()

    giv_seq = generate_sequence(l, sequence_list=test_hiragana)
    for item in giv_seq:
        print(item, end='')
    print()

    i = input().split(' ')
    print(check_inputted_sequence(i, giv_seq, dict=constants.romaji_dict))

    colorama.deinit()

# TODO:
# make sure the zip() in check sequence always defaults to the size of the given sequence, and not the inputted one
# make newline characters as well as spaces act as a word separators (for romaji only)