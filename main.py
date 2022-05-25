import random

hiragana_dict = {
    "a": 'あ',
    "i": 'い',
    "u": 'う',
    "e": 'え',
    "o": 'お',
    "ka": 'か',
    "ki": 'き',
    "ku": 'く',
    "ke": 'け',
    "ko": 'こ',
    "sa": 'さ',
    "shi": 'し',
    "su": 'す',
    "se": 'せ',
    "so": 'そ',
    "ta": 'た',
    "chi": 'ち',
    "tsu": 'つ',
    "te": 'て',
    "to": 'と',
    "na": 'な',
    "ni": 'に',
    "nu": 'ぬ',
    "ne": 'ね',
    "no": 'の',
    "ha": 'は',
    "hi": 'ひ',
    "fu": 'ふ',
    "he": 'へ',
    "ho": 'ほ',
    "ma": 'ま',
    "mi": 'み',
    "mu": 'む',
    "me": 'め',
    "mo": 'も',
    "ya": 'や',
    "yu": 'ゆ',
    "yo": 'よ',
    "ra": 'ら',
    "ri": 'り',
    "ru": 'る',
    "re": 'れ',
    "ro": 'ろ',
    "wa": 'わ',
    "wo": 'を',
    "n": 'ん'
}

romaji = ("a", "i", "u", "e", "o", "ka", "ki", "ku", "ke", "ko", "sa", "shi", "su", "se", "so", "ta", "chi", "tsu", "te", "to", "na", "ni", "nu", "ne", "no", "ha", "hi", "fu", "he", "ho", "ma", "mi", "mu", "me", "mo", "ya", "yu", "yo", "ra", "ri", "ru", "re", "ro", "wa", "wo", "n")

def generate_romaji_sequence(length: int, romaji_list=None):
    if romaji_list is None:
        romaji_list = romaji
    romaji_list_len = len(romaji_list)

    seq_romaji = ""

    for i in range(0, length):
        rand_romaji = romaji_list[random.randint(0, romaji_list_len - 1)]
        seq_romaji = seq_romaji + rand_romaji  + (" " if i != length - 1 else "")

    return seq_romaji

print(generate_romaji_sequence(1000, romaji_list=romaji))
