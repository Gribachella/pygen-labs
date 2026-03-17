from secrets import choice
from random import shuffle
from os import system, name
from sys import exit

# Ф-ия принимает выбранный пользователем алфавит и длину пароля, генерирует и возвращает пароль
def get_uniq_charsets(charset, user_charset):
    combine = [i.copy() for i in charset] + [j.copy() for j in user_charset]
    uniq_charsets = []

    for i in range(len(combine)):
        uniq_chars = []
        
        for j in combine[i]:
            if j not in uniq_chars:
                uniq_chars.append(j)

            for k in range(i + 1, len(combine)):
                combine[k] = [m for m in combine[k] if m != j]

        uniq_charsets.append(uniq_chars.copy())

    while [] in uniq_charsets:
        uniq_charsets.remove([])

    return uniq_charsets

def get_password(length, charset, user_charset, ambiguous, ambiguous_include, space_include):
    uniq_charsets = get_uniq_charsets(charset, user_charset)
    full_password_alphabet = ''.join(get_processed_alphabet(uniq_charsets, 'full'))
    finally_password_alphabet = ''
    
    if not ambiguous_include:
        for sym in full_password_alphabet:
            if sym not in ambiguous:
                finally_password_alphabet += sym
    else:
        finally_password_alphabet = full_password_alphabet

    if space_include:
        finally_password_alphabet += ' '

    finally_password_alphabet = list(finally_password_alphabet)
    
    shuffle(finally_password_alphabet)

    while True:
        password = ''.join([choice(finally_password_alphabet) for _ in range(length)])
        password_in_charsets = True

        if length > len(uniq_charsets):
            for cs in uniq_charsets:
                for sym in password:
                    if sym in cs:
                        break
                else:
                    password_in_charsets = False

            if password_in_charsets:
                break

        else:
            counter = 0
            for cs in uniq_charsets:
                for sym in password:
                    if sym in cs:
                        counter += 1
                        break

            if counter == length:
                break

    return password

# Очищает содержимое консоли улучшая визуал
def clear_console():
    if name == 'nt':
        system('cls')
    else:
        system('clear')

# Рекомендации по наиболее удачному использованию программы
def tips(option):
    if option == "length":
        print(
f'''{'=' * 28}Справочная информация{'=' * 28}
- Минимально рекомендуемая длина пароля - в диапазоне от 12 до 14 символов. 
- Наиболее надежным считается пароль от 18 символов.
- Допустимый ввод: от 4 до 128
{'=' * 77}\n'''
        )

    elif option == 'alphabet':
        print(
f'''{'=' * 28}Справочная информация{'=' * 28}
- Если нет необходимости, крайне рекомендуется оставлять составные части
стандартного набора алфавита пароля включенными. 
- При желании расширить алфавит пароля учитывайте локальную политику паролей.
- [СН] - Стандартный набор.
- Выключая опцию №6 неоднозначные символы будут исключенны из алфавита
пароля в момент генерации пароля, поэтому исключенные неоднозначные
символы все еще смогут отображаться как ВКЛЮЧЕНЫЕ в алфавит в меню.
{'=' * 77}\n'''
        )
    
    elif option == 'user`s charset':
        print(
f'''{'=' * 28}Справочная информация{'=' * 28}
- В опциях 0 и 1 всегда будут находиться функции возвращения в меню выбора 
набора символов и добавления нового пользовательского набора символов
соответственно. А в последующих будут находиться ваши, уже добавленные, наборы 
символов, выбрав которые вы сможете их либо удалить, либо редактировать.
- При генерации пароля конечный алфавит будет формироваться только из
уникальных символов в единичном экземпляре, учитывайте это при составлении
своих наборов символов.
{'=' * 77}\n'''
        )

    elif option == 'add charset':
        print(
f'''{'=' * 28}Справочная информация{'=' * 28}
- В введеном вами наборе символов все дополнительные вхождения одного 
уникального символа будут удалены.
- Набор символов вводиться одной строкой, без пробелов (пробелы выбираются в
меню выбора набора символов опцией №7) и других разделительных знаков между 
символами.
- Не менее 2-х уникальных символов
{'=' * 77}\n'''
        )

    elif option == 'edit charset':
        print(
f'''{'=' * 31}Справочная информация{'=' * 31}
- Вы находитесь в редакторе выбранного набора символов. "Редактор", по-сути, является
заместителем одного набора символов на другой. Так что если хотите подправить 
выбранный набор, то сначала скопируйте и вставьте в терминал исходный набор.
- Если вы введете пустую строку, то набор символов удалится.
- Для редактора набора символов по-прежнему актуальны правила добавления набора символов:
    1) Только уникальные символы, если нет, то программа сама перепишет строку.
    2) Набор вписывается одной строкой без разделительных знаков (пробелов в том числе).
    3) Не менее 2-х уникальных символов в наборе.
    4) Наличие пробела настраивается не тут, а в меню выбора набора символов в опции №7,
    все вписанные в набор пробелы будут удалены.
{'=' * 83}\n'''
        )

    elif option == 'quantity':
        print(
f'''{'=' * 31}Справочная информация{'=' * 31}
- Ввод ограничен диапазоном от 1 до 20.
{'=' * 83}\n'''
        )

# Ф-ия валидации пользовательского ввода, в вопросах предполагаюших численный ответ
def is_valid_digit_answer(answer, x1, x2):
    if answer.isdigit():
        return int(answer) in range(x1, x2 + 1)
    else:
        return False

# Ф-ия валидации пользовательского ввода, в вопросах предполагаюших буквенно-символьный ответ
def is_valid_string_answer(answer, format='yesno'):
    if answer.isalpha():
        if format == 'yesno':
            return answer in ["да", "д", "lf", "l", "y", "yes", "d", "da", "ytn", "net", "no", "n", "нет", "не", "н", "ne"]
    else:
        return False

def filter_charset(charset, set):
    digits = [str(n) for n in range(0, 10)]
    lowercase_letters = [chr(c) for c in range(97, 123)]
    uppercase_letters = [chr(c) for c in range(65, 91)]
    spec_chars = list('!#$%&*+-=?@^_')
    spec_chars_expanded = list("'\"(),./:;<>[\\]`{|}~")

    if set == 'digits':
        set = digits
    elif set == 'lc_letters':
        set = lowercase_letters
    elif set == 'uc_letters':
        set = uppercase_letters
    elif set == 'sp_chars':
        set = spec_chars
    else:
        set = spec_chars_expanded
    
    if set in charset:
        charset.remove(set)
    else:
        charset.append(set)

    return charset

def add_user_charset(user_charset, charset):
    while True:
        clear_console()

        tips('add charset')
        new_charset = input('>>> ').replace(' ', '')
        processed_charset = ''

        for char in new_charset:
            if char not in processed_charset:
                processed_charset += char

        if len(processed_charset) <= 1:
            continue

        proced_charset = list(processed_charset)

        if is_charset_in_alphabet(proced_charset, charset + user_charset):
            clear_console()
            print("Такой набор символов уже есть в алфавите пароля.")
            input('>>> ')
            continue

        return list(processed_charset)

def edit_user_charset(user_charset_index, user_charset, charset):
    while True:
        clear_console()
        tips('edit charset')

        print(f'ИСХОДНЫЙ НАБОР >>> {''.join(user_charset_index)}', end='\n\n')

        new_charset = input('ИЗМЕНЕННЫЙ НАБОР >>> ').replace(" ", '')
        processed_charset = ''

        for char in new_charset:
            if char not in processed_charset:
                processed_charset += char

        if len(processed_charset) <= 1 and new_charset != '':
            continue

        proced_charset = list(processed_charset)

        if is_charset_in_alphabet(proced_charset, charset + user_charset) and proced_charset != user_charset_index:
            clear_console()
            print("Такой набор символов уже есть в алфавите пароля.")
            input('>>> ')
            continue

        return proced_charset

def get_user_charset(user_charset, charset):
    while True:
        charsets_list = get_processed_alphabet(user_charset, 'short').split()
        clear_console()

        tips('user`s charset')
        print('0) Назад')
        print('1) Добавить набор символов')
        for i in range(len(user_charset)):
            print(f'{i + 2}) {charsets_list[i]}')
        
        answer = input('>>> ').strip()

        if not is_valid_digit_answer(answer, 0, len(user_charset) + 1):
            continue

        if answer == "0":
            return user_charset
        elif answer == "1":
            user_charset.append(add_user_charset(user_charset, charset))
        else:
            user_charset[int(answer) - 2] = edit_user_charset(user_charset[int(answer) - 2], user_charset, charset)
            if not user_charset[int(answer) - 2]:
                user_charset.remove([])

def is_charset_in_alphabet(curr_set, gen_charset):
    curr_set_copy = sorted(curr_set)
    gen_charset_copy = [sorted(cs) for cs in gen_charset]

    return curr_set_copy in gen_charset_copy

# Ф-ия, в которой пользователь выбирает набор символов для пароля и может предложить свой набор
def get_password_charset(charset, ambiguous_include, space_include, user_charset):
    digits = [str(n) for n in range(0, 10)]
    lowercase_letters = [chr(c) for c in range(97, 123)]
    uppercase_letters = [chr(c) for c in range(65, 91)]
    spec_chars = list('!#$%&*+-=?@^_')
    spec_chars_expanded = list("'\"(),./:;<>[\\]`{|}~")
    ambiguous = '0Ooi1lI'

    while True:
        combine = charset + user_charset
        full_combine = get_processed_alphabet(charset + user_charset, 'full')
        clear_console()

        tips('alphabet')
        print(f'1) [СН] Цифры {digits[0]}-{digits[-1]}{" " * 27} > {'ВКЛЮЧЕНО' if digits in combine else 'НЕ ВКЛЮЧЕНО'}')
        print(f'2) [СН] Англ. буквы в нижнем регистре {lowercase_letters[0]}-{lowercase_letters[-1]}{" " * 3} > {'ВКЛЮЧЕНО' if lowercase_letters in combine else 'НЕ ВКЛЮЧЕНО'}')
        print(f'3) [СН] Англ. буквы в верхнем регистре {uppercase_letters[0]}-{uppercase_letters[-1]}{" " * 2} > {'ВКЛЮЧЕНО' if uppercase_letters in combine else 'НЕ ВКЛЮЧЕНО'}')
        print(f'4) [СН] Основные спец. символы {''.join(spec_chars)} > {'ВКЛЮЧЕНО' if spec_chars in charset else 'НЕ ВКЛЮЧЕНО'}')
        print(f'5) Доп. спец. символы {''.join(spec_chars_expanded)}{" " * 3} > {'ВКЛЮЧЕНО' if spec_chars_expanded in combine else 'НЕ ВКЛЮЧЕНО'}')
        print(f'6) [СН] Неоднозначные символы {ambiguous}{" " * 7} > {'ВКЛЮЧЕНО ' if ambiguous_include else 'НЕ ВКЛЮЧЕНО'}')
        print(f'7) Символ пробела " "{" " * 23} > {'ВКЛЮЧЕНО' if space_include else 'НЕ ВКЛЮЧЕНО'}')
        print('8) Добавить свой набор символов')
        print('9) Назад')

        answer = input(">>> ").strip()

        if not is_valid_digit_answer(answer, 1, 9):
            continue
        
        if answer == "1":
            charset = filter_charset(charset, 'digits')
        elif answer == "2":
            charset = filter_charset(charset, 'lc_letters')
        elif answer == "3":
            charset = filter_charset(charset, 'uc_letters')
        elif answer == "4":
            charset = filter_charset(charset, 'sp_chars')
        elif answer == "5":
            charset = filter_charset(charset, 'sp_chars+')
        elif answer == "6":
            if ambiguous_include:
                ambiguous_include = False
            else:
                ambiguous_include = True
        elif answer == "7":
            if space_include:
                space_include = False
            else:
                space_include = True
        elif answer == "8":
            user_charset = get_user_charset(user_charset, charset)
        elif answer == "9":
            return charset, ambiguous_include, space_include, user_charset

        full_combine = get_processed_alphabet(charset + user_charset, 'full')

        if not (charset + user_charset):
            space_include, ambiguous_include = False, False
        else:
            for c in ambiguous:  # Проверка на наличие в алфавите хотя бы одного из символов в строке ambiguous
                if c in get_processed_alphabet(charset + user_charset, 'full'):
                    break
            else:
                ambiguous_include = False

            for c in full_combine:  # Проверка состоит ли текущий алфавит исключительно из символов строки ambiguous
                if c not in ambiguous:
                    break
            else:
                ambiguous_include = True

# Ф-ия, возвращающая длину пароля выбранную пользователем
def get_password_length():
    while True:
        clear_console()
        tips('length')
        answer = input('Введите длину пароля: ').strip()

        if not is_valid_digit_answer(answer, 4, 128):
            continue

        passlen = int(answer)
        if int(answer) < 12:
            clear_console()
            answer = input("Внимание! Пароль менее 12 символов небезопасен.\n\nПродолжить? (д - да; н - нет): ").lower().strip()

            while not is_valid_string_answer(answer):
                clear_console()
                answer = input("Внимание! Пароль менее 12 символов небезопасен.\n\nПродолжить? (д - да; н - нет): ").lower().strip()

            if answer in 'da d yes y lf l д да'.split():
                return passlen
        else:
            return passlen

def get_password_quantity():
    while True:
        clear_console()
        tips('quantity')
        answer = input('Введите желаемое количество генерируемых паролей: ').strip()

        if not is_valid_digit_answer(answer, 1, 20):
            continue

        return int(answer)

# Ф-ия обработки второго аргумента main_menu() - списка наборов символов. Возвращает версию для представления в меню и конечный список всех символов
def get_processed_alphabet(alpha, what_to_return='both'):
    shortened_alpha = ''
    full_alpha = []

    for el in alpha:
        shortened_alpha += f'[{el[0]}-{el[-1]}] '
        full_alpha.extend(el)

    shortened_alpha = shortened_alpha.rstrip()
    shuffle(full_alpha)

    if what_to_return == 'both':
        return full_alpha, shortened_alpha
    elif what_to_return == 'full':
        return full_alpha
    elif what_to_return == 'short':
        return shortened_alpha

def main_menu(length, charset, user_charset, quantity):
    clear_console()

    full_alpha, short_alpha = get_processed_alphabet(charset + user_charset)

    uniq_symbols = ''
    for sym in full_alpha:
        if sym not in uniq_symbols:
            uniq_symbols += sym

    if quantity != 1:
        ending = "и"
    else:
        ending = "ь"

    print(f'{'=' * 31}ГЕНЕРАТОР ПАРОЛЕЙ{'=' * 31}')
    print(f'1) Длина пароля: {length}')
    print(f'2) Алфавит пароля: {short_alpha} - {len(uniq_symbols)} уникальных символов')
    print(f'3) Количество: {quantity}', end='\n\n')

    print(f'Вариативность пароля: {len(uniq_symbols) ** length}', end='\n\n')
    print(f'4) Сгенерировать парол{ending}')
    print('5) Выход')
    print('=' * 79)

digits = [str(n) for n in range(0, 10)]
lowercase_letters = [chr(c) for c in range(97, 123)]
uppercase_letters = [chr(c) for c in range(65, 91)]
spec_chars = list('!#$%&*+-=?@^_')
ambiguous = list('0Ooi1lI')
ambiguous_include, space_include = True, False
user_charset = []

charset = [digits, lowercase_letters, uppercase_letters, spec_chars]
password_len, password_quantity = 14, 5

while True:
    main_menu(password_len, charset, user_charset, password_quantity)

    answer = input(">>> ").strip()

    while not is_valid_digit_answer(answer, 1, 5):
        main_menu(password_len, charset, user_charset, password_quantity)
        answer = input(">>> ").strip()

    if answer == '1':
        password_len = get_password_length()
    elif answer == '2':
        charset, ambiguous_include, space_include, user_charset = get_password_charset(charset, ambiguous_include, space_include, user_charset)
    elif answer == '3':
        password_quantity = get_password_quantity()
    elif answer == '4':
        if not charset + user_charset:
            clear_console()
            print("Алфавит пароля не может быть пустым: добавьте свой набор символов или выберете предложенные наборы.", end='\n\n')
            input('>>> ')
            continue

        clear_console()
        for i in range(password_quantity):
            password = get_password(password_len, charset, user_charset, ambiguous, ambiguous_include, space_include)
            print(f"{i + 1}) {password}")

        input()

    else:
        clear_console()
        exit()