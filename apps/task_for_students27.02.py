import psycopg2

def connect_db():
    try:
        conn = psycopg2.connect(
            dbname='shelters_db',
            user='postgres',
            password='1111',
            host='localhost',
            port=5432
        )
        print('База подключена')
        return conn
    except Exception as e:
        print(f"Ошибка подключения: {e}")
        return None

def add_animal(name, species, breed, age, weight):
    conn = connect_db()
    if conn is None: return None
    try:
        cursor = conn.cursor()
        query = """
                INSERT INTO shelters (name, species, breed, age, weight)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id
                """
        cursor.execute(query, (name, species, breed, age, weight))
        animal_id = cursor.fetchone()[0]
        conn.commit()
        cursor.close() 
        conn.close()
        return animal_id
    except Exception as e:
     print(f"ошибка при добавлении животного: {e}")
     if conn:
        conn.rollback()
        conn.close()

def get_all_animals():
    conn = connect_db()
    if conn is None: return []
    try:
        cursor = conn.cursor()
        query = "SELECT * FROM shelters ORDER BY name DESC"
        cursor.execute(query)
        animals = cursor.fetchall()
        return animals
    except Exception as e:
     print(f"ошибка при показе: {e}")
     if conn:
        conn.rollback()
        conn.close()

def get_animal_by_id(animal_id):
    conn = connect_db()
    if conn is None: return None
    try:
        cursor = conn.cursor()
        query = "SELECT * FROM shelters WHERE id = %s"
        cursor.execute(query, (animal_id,))
        animal = cursor.fetchone()
    except Exception as e:
        print(f"ошибка при показе: {e}")
        if conn:
            conn.close()
            return animal

def delete_animal(animal_id):
    conn = connect_db()
    if conn is None: return
    try:
        cursor = conn.cursor()
        query = "DELETE FROM shelters WHERE id = %s"
        cursor.execute(query, (animal_id,))
        conn.commit()
    except Exception as e:
        print(f"ошибка при удалении: {e}")
        if conn:
            conn.close()
        return None
        
def get_avg_age():
    conn = connect_db()
    if conn is None: return 0
    try:
        cursor = conn.cursor()
        query = "SELECT AVG(age) FROM shelters WHERE age IS NOT NULL"
        cursor.execute(query)
        avg = cursor.fetchone()[0]
        return round(avg, 1) if avg else 0
    except Exception as e:
        print(f"ошибка при счете: {e}")
        if conn:
            conn.close()
            return 0

def get_total_weight():
    conn = connect_db()
    if conn is None: return 0
    try:
        cursor = conn.cursor()
        query = "SELECT SUM(weight) FROM shelters WHERE weight IS NOT NULL"
        cursor.execute(query)
        total = cursor.fetchone()[0]
        return total if total else 0
    except Exception as e:
        print(f"ошибка при получении: {e}")
        if conn:
            conn.close()
            return 0

def print_animals(animals):
    if not animals:
        print('Животные не найдены')
        return
    for a in animals:
        # Порядок: id, name, species, breed, age, weight
        print(f"{a[1]} ({a[2]}) | {a[3]} | {a[4]} лет | {a[5]} кг")

def main():
    while True:
        print('\n=== ПРИЮТ ДЛЯ ЖИВОТНЫХ ===')
        print('1. Добавить животное')
        print('2. Показать всех животных')
        print('3. Найти по ID')
        print('4. Удалить животное')
        print('5. Средний возраст')
        print('6. Общий вес всех животных')
        print('7. Выход')
        
        choice = input('Выберите пункт: ')
        
        if choice == '1':
            name = input('Имя: ')
            species = input('Вид (собака/кошка): ')
            breed = input('Порода: ')
            age = int(input('Возраст (лет): '))
            weight = float(input('Вес (кг): '))
            animal_id = add_animal(name, species, breed, age, weight,)
            if animal_id:
                print(f'Животное добавлено с ID: {animal_id}')
        elif choice == '2':
            animals = get_all_animals()
            print_animals(animals)
        elif choice == '3':
            animal_id = int(input('ID животного: '))
            animal = get_animal_by_id(animal_id)
            if animal:
                print_animals([animal])
        elif choice == '4':
            animal_id = int(input('ID для удаления: '))
            delete_animal(animal_id)
            print('Удалено')
        elif choice == '5':
            avg = get_avg_age()
            print(f'Средний возраст: {avg} лет')
        elif choice == '6':
            total = get_total_weight()
            print(f'Общий вес: {total} кг')
        elif choice == '7':
            break
        else:
            print('Неверный ввод')

if __name__ == '__main__':
    main()