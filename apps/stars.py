def stars_constructor():
    for i in range(11):
        print("*" * i)   

a = input("Нажми 1 чтобы сформировать треугольник: ")

if a == "1": 
    stars_constructor()
else:
    print("Бро, я же сказал нажми 1...")

