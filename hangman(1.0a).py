from random import choice
from sys import exit
from os import system, name

def clear_console():
    if name == 'nt':
        system('cls')
    else:
        system('clear')

def guide(option):
    if option == 'rules':
        print(f"{'=' * 31}Виселица - Hangman{'=' * 31}")
        print("Программа загадывает какое-то слово, а вам нужно его отгадать.")
        print("У вас будет возможность указать букву в загаданном слове, либо же")
        print("ввести слово полностью. Если вы промахнетесь в своей догадке, то")
        print("у вас отниметься одна попытка, и начнется отрисовка виселицы. Если человечек на")
        print("виселице отрисуеться полностью до того, как вы угадаете слово, то вы проиграете.", end='\n\n')
        print("Учтите, что в игре также используеться буква 'Ё'.", end='\n\n')
        print("За некорректный ввод (если вводите то, что уже вводили ранее и если")
        print("в вашем вводе есть что-то кроме букв русского алфавита) попытки не отнимаются.")
        print('=' * 80, end='\n\n')

    elif option == "start":
        print(f"{'=' * 28}Справка к конфигурации игры{'=' * 28}")
        print("В 1-ом параметре игры вы выбираете сколько попыток вам даеться на угадывание слова:")
        print("в обычной продолжительности дается 6 попыток, а в долгой - 10. Соответственно")
        print("отрисовка начинается с самой виселицы.", end="\n\n")
        print("Во 2-ом параметре выбираеться отображение подсказки к слову во время игры.", end="\n\n")
        print("В 3-ем параметре вы выбираете начальное состояние первой и последней буквы")
        print("загаданного слова: раскрыты или скрыты.")
        print('=' * 83, end='\n\n')

def get_hangman(tries):
    if tries == 1:
        a = "                ║"
        b = "                ║"
        c = "                ║"
        d = "                ║"
        e = "                ║"
        f = "                ║"
        g = "                ║"
    elif tries == 2:
        a = "                ║"
        b = "                ║"
        c = "                ║"
        d = "                ║"
        e = "|               ║"
        f = "|               ║"
        g = "-               ║"
    elif tries == 3:
        a = "                ║"
        b = "|               ║"
        c = "|               ║"
        d = "|               ║"
        e = "|               ║"
        f = "|               ║"
        g = "-               ║"
    elif tries == 4:
        a = "____            ║"
        b = "|               ║"
        c = "|               ║"
        d = "|               ║"
        e = "|               ║"
        f = "|               ║"
        g = "-               ║"
    elif tries == 5:
        a = "________        ║"
        b = "|      |        ║"
        c = "|               ║"
        d = "|               ║"
        e = "|               ║"
        f = "|               ║"
        g = "-               ║"
    elif tries == 6:
        a = "________        ║"
        b = "|      |        ║"
        c = "|      O        ║"
        d = "|               ║"
        e = "|               ║"
        f = "|               ║"
        g = "-               ║"
    elif tries == 7:
        a = "________        ║"
        b = "|      |        ║"
        c = "|      O        ║"
        d = "|      |        ║"
        e = "|      |        ║"
        f = "|               ║"
        g = "-               ║"
    elif tries == 8:
        a = "________        ║"
        b = "|      |        ║"
        c = "|      O        ║"
        d = "|     \\|        ║"
        e = "|      |        ║"
        f = "|               ║"
        g = "-               ║"
    elif tries == 9:
        a = "________        ║"
        b = "|      |        ║"
        c = "|      O        ║"
        d = "|     \\|/       ║"
        e = "|      |        ║"
        f = "|               ║"
        g = "-               ║"
    elif tries == 10:
        a = "________        ║"
        b = "|      |        ║"
        c = "|      O        ║"
        d = "|     \\|/       ║"
        e = "|      |        ║"
        f = "|     /         ║"
        g = "-               ║"
    elif tries == 11:
        a = "________        ║"
        b = "|      |        ║"
        c = "|      O        ║"
        d = "|     \\|/       ║"
        e = "|      |        ║"
        f = "|     / \\       ║"
        g = "-               ║"

    return a, b, c, d, e, f, g

# Ф-ия возвращает слово в верхнем регистре (строку) и подсказку к слову
def get_word(completed_words_list):
    # Сами категории слов
    professions = """учитель студент инженер депутат хирург фермер биолог министр 
    терапевт агроном""".upper().split()

    animals = """собака птица корова медведь орёл кот лисица дельфин муравей черепаха синица 
    комар стрекоза акула термит ящерица фламинго воробей павлин человек""".upper().split()

    trees = """акация берёза дуб клён сосна ель пихта лиственница липа тополь
    ива ясень каштан бук ольха осина кедр платан яблоня""".upper().split()

    fruits = """яблоко апельсин абрикос ананас персик арбуз груша помидор лимон апельсин""".upper().split()

    city_places = """город дорога магазин библиотека завод океан площадь дворец 
    долина гараж рынок вокзал метро лаборатория музей монастырь булочная пекарня стадион 
    обсерватория галерея пустырь колодец театр""".upper().split()

    nature_places = """озеро дебри океан пустыня берлога нора лужайка""".upper().split()

    household_items = """ножницы зеркало тетрадь ручка жалюзи подушка одеяло кастрюля чемодан портфель 
    рюкзак блокнот щипцы календарь шахматы ключ кошелёк контейнер салфетка полотенце тарелка чашка""".upper().split()

    clothes = """брюки рубашка юбка колготки платье футболка майка свитер кофта толстовка
    куртка пальто шорты джинсы жилет пиджак костюм блузка водолазка шарф шапка кепка перчатки носки""".upper().split()

    art = """скрипка пианино виолончель арфа картина гармония мелодия композиция мольберт поэзия живопись 
    литература кино""".upper().split()

    vehicles = """машина лифт велосипед самолёт троллейбус мотоцикл подлодка парусник ракета""".upper().split()

    electric_appliances = """экран компьютер телефон холодильник кофемашина посудомойка пароварка планшет принтер
    пылесос микроволновка духовка роутер колонка наушники фен вентилятор""".upper().split()

    phenomenon = """сумерки заморозки иллюминация молния туман радуга водопад заря гроза гейзер""".upper().split()

    gems = """рубин сапфир алмаз изумруд топаз аметист гранат жемчуг опал нефрит янтарь""".upper().split()

    substances = """железо кобальт осмий фосфор кремний алюминий магний натрий медь радий титан гелий
    водород углерод кислород марганец вольфрам никель аммиак ацетон глюкоза крахмал целлюлоза этанол""".upper().split()

    shapes = """треугольник ромб квадрат круг овал прямоугольник трапеция параллелограмм
    шестиугольник звезда полумесяц эллипс куб шар конус цилиндр пирамида тор октаэдр""".upper().split()

    space = """звезда горизонт комета космос планета галактика астероид орбита метеор""".upper().split()

    groceries = """консервы макароны""".upper().split()

    # Возвращаемые с категорией подсказки
    hints = [
        "Это какая-то профессия!",
        "Животное.",
        "Тут у нас дерево.",
        "Ну явно же плод какой-нибудь.",
        "Такое место можно найти в городе.",
        "Природная локация.",
        "Бытовая вещь.",
        "Одежда или её элемент.",
        "Искусство!",
        "На этом можно перемещаться.",
        "Электроприбор.",
        "Природное явление.",
        "Драгоценный камень.",
        "Вещество.",
        "Геометрическая фигура.",
        "Эта явно что-то из космоса.",
        "Это что-то съестное."
    ]

    categories = [
        professions, animals, trees, fruits, city_places, nature_places, household_items, clothes, art, vehicles,
        electric_appliances, phenomenon, gems, substances, shapes, space, groceries
    ]

    while True:
        choiced_category = choice(categories)
        category_hint = hints[categories.index(choiced_category)]
        choiced_word = choice(choiced_category)

        if choiced_word in completed_words_list:
            continue
        else:
            break
    
    return choiced_word, category_hint

def bool_switch(bool):
    return not bool

def is_valid_digit_answer(answer, x1, x2):
    if answer.isdigit():
        if not (len(answer) != 1 and answer[0] == '0'):
            return int(answer) in range(x1, x2 + 1)
        else:
            return False
    else:
        return False

def is_valid_string_answer(answer, format='yesno', gameword=''):
    if answer.isalpha():
        if format == 'yesno':
            return answer in 'lf l da d y yes ye да д нет не н net ne n no ytn yt'.split()
        
        elif format == 'game':
            if len(answer) == 1:
                return True
            elif len(answer) == len(gameword):
                return True
            else:
                return False
            
        else:
            return False
    else:
        return False

def before_game_menu(game_duration, hint_status, frst_and_lst_letters_status):
    while True:
        clear_console()
        print(f"1) Продолжительность игры             >  {'ОБЫЧНАЯ' if game_duration else 'ДОЛГАЯ'}")
        print(f"2) Играть с подсказкой                >  {'ДА' if hint_status else 'НЕТ'}")
        print(f"3) Раскрыть первую и последную букву  >  {'ДА' if frst_and_lst_letters_status else 'НЕТ'}", end='\n\n')
        print("4) Правила игры")
        print("5) Играть")
        print("6) Выход")

        answer = input(">>> ").strip()

        if not is_valid_digit_answer(answer, 1, 6):
            continue

        if answer == "1":
            game_duration = bool_switch(game_duration)
        elif answer == "2":
            hint_status = bool_switch(hint_status)
        elif answer == "3":
            frst_and_lst_letters_status = bool_switch(frst_and_lst_letters_status)
        elif answer == "4":
            clear_console()
            guide('rules')
            input(">>> ")
        elif answer == "5":
            break
        else:
            clear_console()
            exit()

    return game_duration, hint_status, frst_and_lst_letters_status

def after_game():
    while True:
        clear_console()
        answer = input("Хотите сыграть еще раз? (д = да; н = нет)\n\n>>> ").strip().lower()

        if not is_valid_string_answer(answer):
            continue

        if answer in "lf l da d y yes ye да д".split():
            while True:
                clear_console()
                answer = input("Хотите поменять конфигурацию игры? (д = да; н = нет)\n\n>>> ").strip().lower()

                if not is_valid_string_answer(answer):
                    continue

                if answer in "lf l da d y yes ye да д".split():
                    return 1
                else:
                    return 2
        else:
            return 3

# Ф-ия возвращает слово с нижними подчеркиванием вместо букв, если их нет в переданном списке букв во 2 параметре. Так же
def get_processed_word(word, letters_list, frst_and_lst_letters_status):  # В параметр letters_list передается список угаданных букв, которые есть в слове
    processed_word = ''

    for lt in word:
        if lt in letters_list:
            processed_word += lt
        else:
            processed_word += '_'

    if frst_and_lst_letters_status:
        processed_word = word[0] + processed_word[1:-1] + word[-1]

    return processed_word
    
def play_the_game(word, game_duration, hint_status, hint, frst_and_lst_letters_status):
    ru_low_letters = [chr(i) for i in range(1072, 1104)] + ['ё']
    correct_letters = []
    mistakes = []
    the_game_is_over = False
    full_word_win = False

    if game_duration:
        attempts = 5
    else:
        attempts = 1

    while True:
        clear_console()
        a, b, c, d, e, f, g = get_hangman(attempts)
        fin_word = get_processed_word(word, correct_letters, frst_and_lst_letters_status)

        if fin_word == word or attempts == 11:
            the_game_is_over = True

        print('═' * 16, '╦', '═' * 38, sep='')
        print(a, (f"{'Подсказка: ' + hint}" if hint_status else f"Слово: {' '.join(fin_word)}") if not the_game_is_over else "Вы победили!" if full_word_win or fin_word == word else "Вы проиграли.")
        print(b)
        print(c, (f"Слово: {' '.join(fin_word)}" if hint_status else "") if not the_game_is_over else "")
        print(d, (f"Ошибки: {', '.join(mistakes)}" if not hint_status else "") if not the_game_is_over else f"Загаданное слово: {word}")
        print(e, (f"Ошибки: {', '.join(mistakes)}" if hint_status else "") if not the_game_is_over else "")
        print(f)
        print(g, f"Осталось попыток: {11 - attempts}" if not the_game_is_over else "")
        print('═' * 16, '╩', '═' * 38, sep='')

        answer = input('>>> ').strip().lower()

        if the_game_is_over:
            break
        elif not is_valid_string_answer(answer, "game", word):
            clear_console()
            input("НЕКОРРЕКТНЫЙ ВВОД: Допустимым ответом является 1 буква, либо же \nнабор букв равный длине загаданного слова. Буквы из русского алфавита. \n\n>>> ")
            continue
        elif answer in mistakes or answer.upper() in correct_letters:
            clear_console()
            print(f"НЕКОРРЕКТНЫЙ ВВОД: Вы уже вводили эт{'у букву' if len(answer) == 1 else 'о слово'}.", end='\n\n')
            input(">>> ")
            continue
        elif len(answer) == 1 and answer not in ru_low_letters:
            clear_console()
            print("НЕКОРРЕКТНЫЙ ВВОД: Только буквы из русского алфавита (+ 'ё')!", end='\n\n')
            input(">>> ")
            continue

        if len(answer) == 1:
            if answer.upper() in word:
                correct_letters.append(answer.upper())
            else:
                mistakes.append(answer)
                attempts += 1

        elif len(answer) == len(word):
            if answer.upper() == word:
                the_game_is_over = True
                full_word_win = True
                continue
            else:
                mistakes.append(answer)
                attempts += 1

game_duration = True  # True - Обычная игра; False - Долгая игра
hint_status = False
frst_and_lst_letters_status = False
completed_words = []

while True:
    game_duration, hint_status, frst_and_lst_letters_status = before_game_menu(game_duration, hint_status, frst_and_lst_letters_status)

    while True: 
        word, hint = get_word(completed_words)
        completed_words += [word]

        play_the_game(word, game_duration, hint_status, hint, frst_and_lst_letters_status)

        user_choice = after_game()

        if user_choice == 1:
            break
        elif user_choice == 2:
            continue
        else:
            clear_console()
            exit()