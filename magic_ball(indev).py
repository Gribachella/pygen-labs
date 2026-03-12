from random import choice, randrange
def txt_to_leet(txt):
    crypted_txt = "A 6 B r g e E }|{ 3 u `u K JI M H 0 TT p c m y cp X LL 4 LLI LLL `b bI b € IO 9I , . ! ? : ;".split() + [' ']
    text = "а б в г д е ё ж з и й к л м н о п р с т у ф х ц ч ш щ ъ ы ь э ю я , . ! ? : ;".split() + [' ']
    converted = ''

    for c in txt:
        if c in text:
            converted += crypted_txt[text.index(c)]

    return converted

def 