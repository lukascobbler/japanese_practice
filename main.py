import random

romaji_dict = {
    "a": "あ",
    "i": "い",
    "u": "う",
    "e": "え",
    "o": "お",
    "ka": "か",
    "ga": "が",
    "ki": "き",
    "gi": "ぎ",
    "ku": "く",
    "gu": "ぐ",
    "ke": "け",
    "ge": "げ",
    "ko": "こ",
    "go": "ご",
    "kya": "きゃ",
    "gya": "ぎゃ",
    "kyu": "きゅ",
    "gyu": "ぎゅ",
    "kyo": "きょ",
    "gyo": "ぎょ",
    "sa": "さ",
    "za": "ざ",
    "shi": "し",
    "ji": "ぢ",
    "su": "す",
    "zu": "づ",
    "se": "せ",
    "ze": "ぜ",
    "so": "そ",
    "zo": "ぞ",
    "sha": "しゃ",
    "ja": "ぢゃ",
    "shu": "しゅ",
    "ju": "ぢゅ",
    "sho": "しょ",
    "jo": "ぢょ",
    "ta": "た",
    "da": "だ",
    "chi": "ち",
    "tsu": "つ",
    "te": "て",
    "de": "で",
    "to": "と",
    "do": "ど",
    "cha": "ちゃ",
    "chu": "ちゅ",
    "cho": "ちょ",
    "na": "な",
    "ni": "に",
    "nu": "ぬ",
    "ne": "ね",
    "no": "の",
    "nya": "にゃ",
    "nyu": "にゅ",
    "nyo": "にょ",
    "ha": "は",
    "ba": "ば",
    "pa": "ぱ",
    "hi": "ひ",
    "bi": "び",
    "pi": "ぴ",
    "fu": "ふ",
    "bu": "ぶ",
    "pu": "ぷ",
    "he": "へ",
    "be": "べ",
    "pe": "ぺ",
    "ho": "ほ",
    "bo": "ぼ",
    "po": "ぽ",
    "hya": "ひゃ",
    "bya": "びゃ",
    "pya": "ぴゃ",
    "hyu": "ひゅ",
    "byu": "びゅ",
    "pyu": "ぴゅ",
    "hyo": "ひょ",
    "byo": "びょ",
    "pyo": "ぴょ",
    "ma": "ま",
    "mi": "み",
    "mu": "む",
    "me": "め",
    "mo": "も",
    "mya": "みゃ",
    "myu": "みゅ",
    "myo": "みょ",
    "ya": "や",
    "yu": "ゆ",
    "yo": "よ",
    "ra": "ら",
    "ri": "り",
    "ru": "る",
    "re": "れ",
    "ro": "ろ",
    "rya": "りゃ",
    "ryu": "りゅ",
    "ryo": "りょ",
    "wa": "わ",
    "wo": "を",
    "n": "ん"
}

hiragana_dict = {
    'あ': 'a',
    'い': 'i',
    'う': 'u',
    'え': 'e',
    'お': 'o',
    'か': 'ka',
    'が': 'ga',
    'き': 'ki',
    'ぎ': 'gi',
    'く': 'ku',
    'ぐ': 'gu',
    'け': 'ke',
    'げ': 'ge',
    'こ': 'ko',
    'ご': 'go',
    'きゃ': 'kya',
    'ぎゃ': 'gya',
    'きゅ': 'kyu',
    'ぎゅ': 'gyu',
    'きょ': 'kyo',
    'ぎょ': 'gyo',
    'さ': 'sa',
    'ざ': 'za',
    'し': 'shi',
    'じ': 'ji',
    'す': 'su',
    'ず': 'zu',
    'せ': 'se',
    'ぜ': 'ze',
    'そ': 'so',
    'ぞ': 'zo',
    'しゃ': 'sha',
    'じゃ': 'ja',
    'しゅ': 'shu',
    'じゅ': 'ju',
    'しょ': 'sho',
    'じょ': 'jo',
    'た': 'ta',
    'だ': 'da',
    'ち': 'chi',
    'ぢ': 'ji',
    'つ': 'tsu',
    'づ': 'zu',
    'て': 'te',
    'で': 'de',
    'と': 'to',
    'ど': 'do',
    'ちゃ': 'cha',
    'ぢゃ': 'ja',
    'ちゅ': 'chu',
    'ぢゅ': 'ju',
    'ちょ': 'cho',
    'ぢょ': 'jo',
    'な': 'na',
    'に': 'ni',
    'ぬ': 'nu',
    'ね': 'ne',
    'の': 'no',
    'にゃ': 'nya',
    'にゅ': 'nyu',
    'にょ': 'nyo',
    'は': 'ha',
    'ば': 'ba',
    'ぱ': 'pa',
    'ひ': 'hi',
    'び': 'bi',
    'ぴ': 'pi',
    'ふ': 'fu',
    'ぶ': 'bu',
    'ぷ': 'pu',
    'へ': 'he',
    'べ': 'be',
    'ぺ': 'pe',
    'ほ': 'ho',
    'ぼ': 'bo',
    'ぽ': 'po',
    'ひゃ': 'hya',
    'びゃ': 'bya',
    'ぴゃ': 'pya',
    'ひゅ': 'hyu',
    'びゅ': 'byu',
    'ぴゅ': 'pyu',
    'ひょ': 'hyo',
    'びょ': 'byo',
    'ぴょ': 'pyo',
    'ま': 'ma',
    'み': 'mi',
    'む': 'mu',
    'め': 'me',
    'も': 'mo',
    'みゃ': 'mya',
    'みゅ': 'myu',
    'みょ': 'myo',
    'や': 'ya',
    'ゆ': 'yu',
    'よ': 'yo',
    'ら': 'ra',
    'り': 'ri',
    'る': 'ru',
    'れ': 're',
    'ろ': 'ro',
    'りゃ': 'rya',
    'りゅ': 'ryu',
    'りょ': 'ryo',
    'わ': 'wa',
    'を': 'wo',
    'ん': 'n'
}

romaji = (
'a', 'i', 'u', 'e', 'o', 'ka', 'ga', 'ki', 'gi', 'ku', 'gu', 'ke', 'ge', 'ko', 'go', 'kya', 'gya', 'kyu', 'gyu', 'kyo',
'gyo', 'sa', 'za', 'shi', 'ji', 'su', 'zu', 'se', 'ze', 'so', 'zo', 'sha', 'ja', 'shu', 'ju', 'sho', 'jo', 'ta', 'da',
'chi', 'tsu', 'te', 'de', 'to', 'do', 'cha', 'chu', 'cho', 'na', 'ni', 'nu', 'ne', 'no', 'nya', 'nyu', 'nyo', 'ha',
'ba', 'pa', 'hi', 'bi', 'pi', 'fu', 'bu', 'pu', 'he', 'be', 'pe', 'ho', 'bo', 'po', 'hya', 'bya', 'pya', 'hyu', 'byu',
'pyu', 'hyo', 'byo', 'pyo', 'ma', 'mi', 'mu', 'me', 'mo', 'mya', 'myu', 'myo', 'ya', 'yu', 'yo', 'ra', 'ri', 'ru', 're',
'ro', 'rya', 'ryu', 'ryo', 'wa', 'wo', 'n')
hiragana = (
'あ', 'い', 'う', 'え', 'お', 'か', 'が', 'き', 'ぎ', 'く', 'ぐ', 'け', 'げ', 'こ', 'ご', 'きゃ', 'ぎゃ', 'きゅ', 'ぎゅ', 'きょ', 'ぎょ', 'さ', 'ざ',
'し', 'じ', 'す', 'ず', 'せ', 'ぜ', 'そ', 'ぞ', 'しゃ', 'じゃ', 'しゅ', 'じゅ', 'しょ', 'じょ', 'た', 'だ', 'ち', 'ぢ', 'つ', 'づ', 'て', 'で', 'と',
'ど', 'ちゃ', 'ぢゃ', 'ちゅ', 'ぢゅ', 'ちょ', 'ぢょ', 'な', 'に', 'ぬ', 'ね', 'の', 'にゃ', 'にゅ', 'にょ', 'は', 'ば', 'ぱ', 'ひ', 'び', 'ぴ', 'ふ',
'ぶ', 'ぷ', 'へ', 'べ', 'ぺ', 'ほ', 'ぼ', 'ぽ', 'ひゃ', 'びゃ', 'ぴゃ', 'ひゅ', 'びゅ', 'ぴゅ', 'ひょ', 'びょ', 'ぴょ', 'ま', 'み', 'む', 'め', 'も',
'みゃ', 'みゅ', 'みょ', 'や', 'ゆ', 'よ', 'ら', 'り', 'る', 'れ', 'ろ', 'りゃ', 'りゅ', 'りょ', 'わ', 'を', 'ん')

test_hiragana = ('あ', 'い', 'う', 'え', 'お', 'か', 'き', 'く', 'け', 'こ')


def generate_sequence(length: int, sequence_list: tuple = None):
    if sequence_list is None:
        sequence_list = hiragana
    sequence_list_len = len(sequence_list)

    sequence = []
    for i in range(0, length):
        rand_char = sequence_list[random.randint(0, sequence_list_len - 1)]
        sequence.append(rand_char)

    return sequence


def check_inputted_sequence(inputted_sequence, given_sequence, dict=None):
    if dict is None:
        dict = romaji_dict
    for inp_word, giv_word in zip(inputted_sequence, given_sequence):
        # print(inp_word, giv_word)
        try:
            if dict[inp_word] != giv_word:
                return False
        except KeyError:
            return False

    return True


while True:
    l = 3
    giv_seq = generate_sequence(3, sequence_list=test_hiragana)
    print(giv_seq)
    seq = []
    while l > 0:
        i = input()
        seq.append(i)
        l -= 1
    print(seq)
    print(check_inputted_sequence(seq, giv_seq, dict=romaji_dict))

# TODO:
# make sure the zip() in check sequence always defaults to the size of the given sequence, and not the inputted one
# move all the constants (dicts, char lists) to one file
# display better output (show a string instead of a list)
# make newline characters as well as spaces act as a word separators (for romaji only)