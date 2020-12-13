def SaveFile(result,type):
    actSave = int(input('Желаете сохранить результат?\n'
                    '1 - Да\n'
                    '2 - Нет\n'))
    if actSave == 1:
        if type == 1:
            file = open("results/result.txt", "w")
            file.write(str(result))
            file.close()
