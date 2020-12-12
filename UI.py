import sys

from translator import translate_text, translate_file


def chooseMethod():
    chooseAct = int(input('Выберите источник текста:\n'
                    '1 - Ручной ввод\n'
                    '2 - Файл\n'
                    '3 - Выход\n'))
    if chooseAct == 1:
        translate_text(input('Введите текст: '))
    elif chooseAct == 2:
        translate_file(input('Введите путь к файлу'))
    elif chooseAct == 3:
        print('До новых встреч!')
        sys.exit()


def expectation():
    while True:
        act = int(input('Желаете продолжить?\n'
                        '1 - Да\n'
                        '2 - Нет\n'))
        if act == 1:
            chooseMethod()
        elif act == 2:
            print('До новых встреч!')
            break