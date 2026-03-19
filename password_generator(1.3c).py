from secrets import choice
from random import shuffle
from os import system, name
from sys import exit
from math import log2

# Ф-ия принимает полный список наборов символов, генерирует и возвращает список наборов символов включающих только уникальные символы
def get_uniq_charsets(charset, user_charset, ambiguous_include):
    combine = [i.copy() for i in charset] + [j.copy() for j in user_charset]
    uniq_charsets = []
    ambiguous = '0Ooi1lI'

    for i in range(len(combine)):
        uniq_chars = []
        
        for j in combine[i]:
            if not ambiguous_include:
                if j not in uniq_chars and j not in ambiguous:
                    uniq_chars.append(j)
            else:
                if j not in uniq_chars:
                    uniq_chars.append(j)

            for k in range(i + 1, len(combine)):
                combine[k] = [m for m in combine[k] if m != j]

        uniq_charsets.append(uniq_chars.copy())

    while [] in uniq_charsets:
        uniq_charsets.remove([])

    return uniq_charsets

# Функция генерации пароля + проверка на предмет максимально возможного включения в содержание пароля всех уникальных групп символов
def get_password(length, charset, user_charset, ambiguous, ambiguous_include, space_include):
    uniq_charsets = get_uniq_charsets(charset, user_charset, ambiguous_include)
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
        uniq_charsets += [[' ']]

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
        print(f"{'=' * 28}Справочная информация{'=' * 28}")
        print("- Минимально рекомендуемая длина пароля - в диапазоне от 12 до 14 символов.") 
        print("- Наиболее надежным считается пароль от 18 символов.")
        print("- Допустимый ввод: от 4 до 128")
        print(f"{'=' * 77}\n")

    elif option == 'alphabet':
        print(f"{'=' * 28}Справочная информация{'=' * 28}")
        print("- Если нет необходимости, крайне рекомендуется оставлять составные части")
        print("стандартного набора алфавита пароля включенными.") 
        print("- При желании расширить алфавит пароля учитывайте локальную политику паролей.")
        print("- [СН] - Стандартный набор.")
        print(f"{'=' * 77}\n")
    
    elif option == 'user`s charset':
        print(f"{'=' * 28}Справочная информация{'=' * 28}")
        print("- В опциях 0 и 1 всегда будут находиться функции возвращения в меню выбора ")
        print("набора символов и добавления нового пользовательского набора символов")
        print("соответственно. А в последующих будут находиться ваши, уже добавленные, наборы ")
        print("символов, выбрав которые вы сможете их либо удалить, либо редактировать.")
        print("- При генерации пароля конечный алфавит будет формироваться только из")
        print("уникальных символов в единичном экземпляре, учитывайте это при составлении")
        print("своих наборов символов.")
        print(f"{'=' * 77}\n")

    elif option == 'add charset':
        print(f"{'=' * 28}Справочная информация{'=' * 28}")
        print("- В введеном вами наборе символов все дополнительные вхождения одного ")
        print("уникального символа будут удалены.")
        print("- Набор символов вводиться одной строкой, без пробелов (пробелы выбираются в")
        print("меню выбора набора символов опцией №7) и других разделительных знаков между ")
        print("символами.")
        print("- Не менее 2-х уникальных символов")
        print(f"{'=' * 77}\n")

    elif option == 'edit charset':
        print(f"{'=' * 31}Справочная информация{'=' * 31}")
        print('- Вы находитесь в редакторе выбранного набора символов. "Редактор", по-сути, является')
        print("заместителем одного набора символов на другой. Так что если хотите подправить ")
        print("выбранный набор, то сначала скопируйте и вставьте в терминал исходный набор.")
        print("- Если вы введете пустую строку, то набор символов удалится.")
        print("- Для редактора набора символов по-прежнему актуальны правила добавления набора символов:")
        print("    1) Только уникальные символы, если нет, то программа сама перепишет строку.")
        print("    2) Набор вписывается одной строкой без разделительных знаков (пробелов в том числе).")
        print("    3) Не менее 2-х уникальных символов в наборе.")
        print("    4) Наличие пробела настраивается не тут, а в меню выбора набора символов в опции №7,")
        print("    все вписанные в набор пробелы будут удалены.")
        print(f"{'=' * 83}\n")

    elif option == 'quantity':
        print(f"{'=' * 31}Справочная информация{'=' * 31}")
        print("- Ввод ограничен диапазоном от 1 до 20.")
        print(f"{'=' * 83}\n")

# Ф-ия валидации пользовательского ввода, в вопросах предполагаюших численный ответ
def is_valid_digit_answer(answer, x1, x2):
    if answer.isdigit():
        if len(answer) != 1 and answer[0] == "0":
            return False
        else:
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

# Ф-ия используемая в ф-ии get_password_charset() для включения или выключения из основного списка наборов символов
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

# Ф-ия добавления в пользовательский список наборов символов свой набор символов
def add_user_charset(user_charset, charset):
    digits = [str(n) for n in range(0, 10)]
    lowercase_letters = [chr(c) for c in range(97, 123)]
    uppercase_letters = [chr(c) for c in range(65, 91)]
    spec_chars = list('!#$%&*+-=?@^_')
    spec_chars_expanded = list("'\"(),./:;<>[\\]`{|}~")
    standard_set = [digits] + [lowercase_letters] + [uppercase_letters] + [sorted(spec_chars)] + [sorted(spec_chars_expanded)]

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
        elif sorted(proced_charset) in standard_set:
            clear_console()
            print("Такой набор символов можно выбрать в меню алфавита пароля.")
            input('>>> ')
            continue

        return list(processed_charset)

# Ф-ия редактирования набора символов в пользовательском списке наборов символов
def edit_user_charset(user_charset_index, user_charset, charset):
    digits = [str(n) for n in range(0, 10)]
    lowercase_letters = [chr(c) for c in range(97, 123)]
    uppercase_letters = [chr(c) for c in range(65, 91)]
    spec_chars = list('!#$%&*+-=?@^_')
    spec_chars_expanded = list("'\"(),./:;<>[\\]`{|}~")
    standard_set = [digits] + [lowercase_letters] + [uppercase_letters] + [sorted(spec_chars)] + [sorted(spec_chars_expanded)]

    while True:
        clear_console()
        tips('edit charset')

        print(f'ИСХОДНЫЙ НАБОР >>> {"".join(user_charset_index)}', end="\n\n")

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
        elif sorted(proced_charset) in standard_set:
            clear_console()
            print("Такой набор символов можно выбрать в меню алфавита пароля.")
            input('>>> ')
            continue

        return proced_charset

# Меню взаимодействия пользователя с пользовательским списком наборов символов
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

# Ф-ия проверяет есть ли в полном (пользоватльский + основной) списке наборов символов набор символов переданный в первый параметр ф-ии
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
        print(f'1) [СН] Цифры {digits[0]}-{digits[-1]}{" " * 27} > {"ВКЛЮЧЕНО" if digits in combine else "НЕ ВКЛЮЧЕНО"}')
        print(f'2) [СН] Англ. буквы в нижнем регистре {lowercase_letters[0]}-{lowercase_letters[-1]}{" " * 3} > {"ВКЛЮЧЕНО" if lowercase_letters in combine else "НЕ ВКЛЮЧЕНО"}')
        print(f'3) [СН] Англ. буквы в верхнем регистре {uppercase_letters[0]}-{uppercase_letters[-1]}{" " * 2} > {"ВКЛЮЧЕНО" if uppercase_letters in combine else "НЕ ВКЛЮЧЕНО"}')
        print(f'4) [СН] Основные спец. символы {"".join(spec_chars)} > {"ВКЛЮЧЕНО" if spec_chars in charset else "НЕ ВКЛЮЧЕНО"}')
        print(f'5) Доп. спец. символы {"".join(spec_chars_expanded)}{" " * 3} > {"ВКЛЮЧЕНО" if spec_chars_expanded in combine else "НЕ ВКЛЮЧЕНО"}')
        print(f'6) [СН] Неоднозначные символы {ambiguous}{" " * 7} > {"ВКЛЮЧЕНО" if ambiguous_include else "НЕ ВКЛЮЧЕНО"}')
        print(f'7) Символ пробела " "{" " * 23} > {"ВКЛЮЧЕНО" if space_include else "НЕ ВКЛЮЧЕНО"}')
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
        uniq_full_combine = '' if not space_include else ' '

        for c in full_combine:
            if c not in uniq_full_combine:
                uniq_full_combine += c

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
            
            is_ambiguous_in = False
            counter = 0

            for c in uniq_full_combine:
                if c not in ambiguous:
                    counter += 1
                else:
                    is_ambiguous_in = True
                if counter == 2:
                    break
            else:
                if is_ambiguous_in:
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

# Ф-ия возвращает количество генерируемых паролей
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

# Ф-ия возвращает строку в соответствии с значением показателя энтропии пароля, используется только в главном меню
def get_entropy_case(length, alphabet):
    entropy = round(length * log2(len(alphabet)), 2)

    if entropy < 50:
        return 'Слабый пароль'
    elif 50 <= entropy < 82:
        return 'Средний пароль'
    elif 82 <= entropy < 120:
        return 'Сильный пароль'
    elif 120 <= entropy < 256:
        return 'Очень сильный пароль'
    else:
        return 'Гроверорезистентный пароль'

# Главное меню программы
def main_menu(length, charset, user_charset, quantity, space_include, ambiguous_include):
    clear_console()

    full_alpha, short_alpha = get_processed_alphabet(charset + user_charset)

    uniq_symbols = ''
    for sym in full_alpha:
        if sym not in uniq_symbols:
            uniq_symbols += sym
    
    if space_include:
        uniq_symbols += ' '
    if not ambiguous_include:
        for sym in '0Ooi1lI':
            uniq_symbols = uniq_symbols.replace(sym, '')

    if charset + user_charset:
        entropy = round(length * log2(len(uniq_symbols)), 2)
        entropy_case = get_entropy_case(length, uniq_symbols)
    else:
        entropy = 0

    if quantity != 1:
        ending = "и"
    else:
        ending = "ь"

    print(f'{"=" * 31}ГЕНЕРАТОР ПАРОЛЕЙ{"=" * 31}')
    print(f'1) Длина пароля: {length}')
    print(f"2) Алфавит пароля: {short_alpha}{' + [\" \"]' if space_include else ''} - {len(uniq_symbols)} уникальных символов")
    print(f'3) Количество: {quantity}', end='\n\n')

    print(f'Энтропия пароля: {entropy} бит {"" if not entropy else f"- {entropy_case}"}', end='\n\n')
    print(f'4) Сгенерировать парол{ending}')
    print('5) Выход')
    print('=' * 79)

# Инициализация начальных переменных: динамичных (параметры пароля) и статичных (наборы символов)
digits = [str(n) for n in range(0, 10)]
lowercase_letters = [chr(c) for c in range(97, 123)]
uppercase_letters = [chr(c) for c in range(65, 91)]
spec_chars = list('!#$%&*+-=?@^_')
ambiguous = list('0Ooi1lI')

ambiguous_include, space_include = True, False
user_charset = []
charset = [digits, lowercase_letters, uppercase_letters, spec_chars]
password_len, password_quantity = 14, 5

# Основной цикл программы
while True:
    main_menu(password_len, charset, user_charset, password_quantity, space_include, ambiguous_include)

    answer = input(">>> ").strip()

    while not is_valid_digit_answer(answer, 1, 5):
        main_menu(password_len, charset, user_charset, password_quantity, space_include, ambiguous_include)
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