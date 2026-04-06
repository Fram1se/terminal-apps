import random
from datetime import datetime

# переменные для игры в рулетку:
RED = "red" # первый цвет
BLACK = "black" # второй цвет
ZERO = "0" # ноль для версии рулетки США
ZEROX2 = "00" # два ноля для версии рулетки США
COLOR_VALUES1 = [BLACK, RED] 
COLOR_VALUES2 = [RED, BLACK, ZERO, ZEROX2]
BALIC = 1000 # изначальный баланс игрока

# функция для игры
def roulet_EU():
    global BALIC # используем переменную в глобальном значении что бы не было ошибки(без global будет искать локальную переменную в функции)
    trying = input(f"Выбери {BLACK} или {RED} (для выхода напишите Выход): ")
    if trying == "Выход":
        return main()
    stavka = int(input(f"сколько поставишь денег? Твой баланс {BALIC}: "))
    
    def Random_color():
        return random.choice(COLOR_VALUES1)
    
    result = Random_color()
    print(result)

    if trying == result:
        BALIC += stavka
        print(BALIC)
        return roulet_EU()
    else:
        BALIC -= stavka
        print(BALIC)
        if BALIC <= 0:
            print("у тебя нету денег, ты нам должен.")
        return main()
    
def roulet_USA():
    global BALIC # используем переменную в глобальном значении что бы не было ошибки(без global будет искать локальную переменную в функции)
    trying = input(f"Выбери {BLACK}, {RED}, {ZERO} или {ZEROX2} (для выхода напишите Выход): ")
    if trying == "Выход":
        return main()
    stavka = int(input(f"сколько поставишь денег? Твой баланс {BALIC}: "))
    
    def Random_color():
        return random.choice(COLOR_VALUES2)
    
    result = Random_color()
    print(result)

    if trying == result:
        BALIC += stavka
        print(BALIC)
        return roulet_EU()
    else:
        BALIC -= stavka
        print(BALIC)
        if BALIC <= 0:
            print("у тебя нету денег, ты нам должен.")
        return main()

shot1 = "1"
shot2 = "2"
shot3 = "3"
shot4 = "4"
SHOT_LIST = [shot1, shot2, shot3, shot4]


def Russian_roulet():
    global BALIC
    print("Приветствую тебя на одной из самых жестоких, но самой прибыльной игре")
    ur_shot = input(f"Выбери сколько раз ты нажмешь курок от {shot1} до {shot4}: ")
    stavka = int(input(f"сколько поставишь денег? Твой баланс {BALIC}: "))

    def Random_shot():
        return random.choice(SHOT_LIST)
    
    result = Random_shot()
    print(result)

    if ur_shot >= result:
        print("ТЫ МЕРТВ")
        breakpoint
    elif ur_shot == 2 and result > ur_shot:
        print("Ты выжил")
        BALIC += stavka * 2
        return main()
    elif ur_shot == 3 and result > ur_shot:
        print("Ты выжил")
        BALIC += stavka * 3
        return main()

    
def main():
    print("Приветствую тебя в нашем казино NAEB.com")
    print("1. Рулетка (европейская)")
    print("2. Рулетка (США)")
    print("3. Русская рулетка")
    print("4. Двадцать одно")
    print("5. Выход")
    vvod = int(input("Введи во что ты хочешь поиграть: "))

    if vvod == 1:
        roulet_EU()
    elif vvod == 2:
        roulet_USA()
    elif vvod == 3:
        Russian_roulet()
    elif vvod == 5:
        breakpoint

main()