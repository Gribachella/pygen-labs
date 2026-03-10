from random import randint, choice
from sys import exit
def rules():
    print(
        f"""        {'~' * 31}Добро пожаловать в числовую угадайку!{'~' * 31}
        Правила простые: Программа случайным образом загадывает целое неотрицательное число в предложенном
        вами диапазоне целых неотрицательных чисел (границы включены), а вам нужно это число отгадать. 

        Если вы решите задать собственный диапазон, помните: его границы должны быть
        целыми неотрицательными числами и не должны совпадать. Если левая (1-ая) граница
        окажется больше правой (2-ой), например [3; 1], программа поменяет их значения местами.
        Если вы откажетесь вводить свой диапазон, то вам будут предложены два стандартных варианта. 
        
        Если вы введете число меньше загаданного, то программа вернет вам строку
        оповещающую об этом, то же верно и для случая, когда введённое вами число больше загаданного.
        {'~' * 43}Весёлой игры!{'~' * 43}""", end='\n\n'
    )

# Ф-я принимает границы диапазона и возвращает минимальное количество попыток, за которое в нём гарантированно можно угадать любое число
def guaranteed_attempts(a, b):
    a, b = int(a), int(b)
    counter = 0

    while a <= b:
        middle = (a + b) // 2
        a = middle + 1
        counter += 1

    return counter

# Функция проверяющая недопустимость ответа в вопросах предполагающих ограничное количество вариантов ответа в определенном формате
def is_invalid_answer(answer):
    if answer.isalpha():
        return answer not in ["да", "д", "y", "yes", "da", 'l', 'lf', "нет", "н", "не", "no", "ne", "n", "net", 'ytn']
    elif answer.isdigit():
        return int(answer) not in [1, 2]
    else:
        return True

# Проверяет находиться ли предполагаемое пользователем число в диапазоне чисел, если да: вовзращает True, нет - False
def is_num_in_range(x, y, num):
    if num.isdigit():
        if int(x) <= int(num) <= int(y):
            return True
    return False

# Проверка отсекающая: отрицательные числа, рациональные числа, "числа" начинающиеся с нуля, продолжающиеся отличными цифрами и не числа
def is_valid_num(num):
    if num.isdigit():
        if len(num) == 1 and num[0] == "0":
            return True
        elif num[0] != "0":
            return True
        else:
            return False
    return False

# Подготовка к началу игры - выбор диапазона секретного числа
def get_range():
    answer = input("Вы хотите ввести свой диапазон чисел? (д = да; н = нет): ").lower().strip()

    while is_invalid_answer(answer):
        answer = input("Возможные варианты ответа: д = да; н = нет: ").lower().strip()

    if answer in ["да", "д", "y", "yes", "da", 'l', 'lf']:

        a = input("Введите левую границу: ").strip()
        while not is_valid_num(a):
            print('Я же сказал, что границы должны быть целыми неотрицательными числами...')
            a = input("Введите левую границу: ")

        b = input("Введите правую границу: ").strip()
        while not is_valid_num(b) or b == a:
            if b == a:
                print('Я же сказал, что границы должны быть разными числами...')
            else:
                print('Я же сказал, что границы должны быть целыми неотрицательными числами...')
            b = input("Введите правую границу: ")

        print()

        if int(a) > int(b):
            a, b = b, a
        return a, b

    else:
        option1, option2 = ["0", "200"], ["0", "1487"]
        print(
            """Выберите диапазон из предложенных стандартных вариантов
            1) от 0 до 200
            2) от 0 до 1487"""
        )
        selection = input("первый вариант = 1; второй вариант = 2: ").strip()

        while is_invalid_answer(selection) or not selection.isdigit():
            print(
                """Возможные варианты:
                1) от 0 до 200
                2) от 0 до 1487"""
            )
            selection = input("первый вариант = 1; второй вариант = 2: ").strip()

        print()

        if selection == '1':
            return option1[0], option1[1]
        else:
            return option2[0], option2[1]

# Приглашение в игру
answer = input("Привет! Не желаешь сыграть в игру? (д = да; н = нет): ").lower().strip()

while is_invalid_answer(answer) or not answer.isalpha():
    answer = input("Возможные варианты ответа: д = да; н = нет: ").lower().strip()

if answer in ["да", "д", "y", "yes", "da", 'l', 'lf']:
    print("Ура! В таком случае сейчас расскажу правила...", end='\n\n')
    rules()
else:
    answer = input(f"Как так... ты... правда не хочешь поиграть? {chr(128543)} (д = да, не хочу; н = нет, мне захотелось): ").lower().strip()

    while is_invalid_answer(answer) or not answer.isalpha():
        answer = input("Возможные варианты ответа: да, не хочу; н = нет, мне захотелось: ").lower().strip()

    if answer in ["да", "д", "y", "yes", "da", 'l', 'lf']:
        print('Тогда увидимся в другой раз. Заходи поиграть, когда захочешь.')
        exit()
    else:
        print("Ура! В таком случае сейчас расскажу правила...", end='\n\n')
        rules()

# Основной цикл игры
while True:
    win_notices = ['Вы угадали!', 'Поздравляю, число угадано!', 'Игра окончена, победа за вами!']
    less_notices = ['Это слишком мало!', 'Что-то тут не густо (мало)', 'Маловато', 'Мааааалооооооооооо']
    surplus_notices = ['Тут многовато', 'Слишком много', 'Много! Много! Много!', "Куда столько? (много)"]
    error_notice = ['Такого нет в диапазоне...', 'Вы точно сюда играть пришли?', 'Зачем же ты так...']
    total_win_notices = ['Это что такое, победа?', 'Вы угадали число с первого раза!', 'Вы получили достижение "шулер"']
    long_game_win_phrases = ['Ты вообще старался?', 'Тебе надо больше тренироваться.', '10000011110 10001000001 10000110101 10000111011']
    a, b = get_range()

    attempts = 1
    long_game = guaranteed_attempts(a, b) + guaranteed_attempts(a, b) // 2
    secret_num = randint(int(a), int(b))

    print(f'Я загадал число от {int(a)} до {int(b)}')
    num = input("Введите предполагаемое число: ")

    while True:
        if not is_num_in_range(a, b, num):
            print(choice(error_notice))
            num = input()
            continue
        elif int(num) == secret_num:
            if secret_num == 727:
                print(f'Попытка №{attempts}: https://osu.ppy.sh/scores/453746931')
            elif attempts == 1:
                print(f'Попытка №{attempts}: {choice(total_win_notices)}')
            elif attempts < long_game:
                print(f'Попытка №{attempts}: {choice(win_notices)}')
            else:
                print(f'Попытка №{attempts}: {choice(long_game_win_phrases)}')
            break
        elif int(num) > int(secret_num):
            print(f'Попытка №{attempts}: {choice(surplus_notices)}')
            attempts += 1
            num = input()
        elif int(num) < int(secret_num):
            print(f'Попытка №{attempts}: {choice(less_notices)}')
            attempts += 1
            num = input()
    
    print()

    answer = input('Ну как, весело? Хотите сыграть еще? (д = да; н = нет): ').lower().strip()

    while is_invalid_answer(answer) or not answer.isalpha():
        answer = input("Возможные варианты ответа: д = да; н = нет: ").lower().strip()
    
    if answer in ["да", "д", "y", "yes", "da", 'l', 'lf']:
        print("Класс, поехали по новому кругу!")
    else:
        print('Тогда увидимся в другой раз. Заходи поиграть, когда захочешь.')
        break
