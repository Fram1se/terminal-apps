import psycopg2
from datetime import datetime

def connect_db():
    try:
        conn = psycopg2.connect(
            dbname='getbusy',
            user='postgres',
            password='1111',
            host='localhost',
            port=5432
        )
        print('База тренировок подключена')
        return conn
    except Exception as e:
        print(f"Ошибка подключения: {e}")
        return None

def add_workout(exercise, weight, reps, sets, muscle, notes):
    conn = connect_db()
    if conn is None: return None
    try:
        cursor = conn.cursor()
        query = """
            INSERT INTO workout_logs (exercise, weight, reps, sets, muscle, notes)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id
                """
        cursor.execute(query, (exercise, weight, reps, sets, muscle, notes))
        workout_id = cursor.fetchone()[0]
        conn.commit()
        cursor.close() 
        conn.close()
        return workout_id
    except Exception as e:
     print(f"ошибка при добавлении: {e}")
     if conn:
        conn.rollback()
        conn.close()

def get_all_workouts():
    conn = connect_db()
    if conn is None: return []
    try:
        cursor = conn.cursor()
        query = "SELECT * FROM workout_logs ORDER BY exercise DESC"
        cursor.execute(query)
        workouts = cursor.fetchall()
        return workouts
    except Exception as e:
     print(f"ошибка при получении: {e}")
     if conn:
        conn.close()
        return[]

def search_by_exercise(exercise_name):
    conn = connect_db()
    if conn is None: return []
    try:
        cursor = conn.cursor()
        pattern = f"%{exercise_name}%"
        query = "SELECT * FROM workout_logs WHERE exercise ILIKE %s ORDER BY sets DESC"
        cursor.execute(query, (pattern,))
        workouts = cursor.fetchall()
        return workouts
    except Exception as e:
     print(f"ошибка при поиске: {e}")
     if conn:
        conn.close()
        return[]

def filter_by_muscle(muscle_group):
    conn = connect_db()
    if conn is None: return []
    try:
        cursor = conn.cursor()
        query = "SELECT * FROM workout_logs WHERE muscle = %s ORDER BY exercise DESC"
        cursor.execute(query, (muscle_group,))
        workouts = cursor.fetchall()
        return workouts
    except Exception as e:
     print(f"ошибка при фильтрации: {e}")
     if conn:
        conn.close()
        return[]

def update_workout(log_id, new_weight, new_notes):
    conn = connect_db()
    if conn is None: return
    try:
        cursor = conn.cursor()
        query = "UPDATE workout_logs SET weight = %s, notes = %s WHERE id = %s"
        cursor.execute(query, (new_weight, new_notes, log_id))
        conn.commit()
    except Exception as e:
     print(f"ошибка при обнавлении: {e}")
     if conn:
        conn.rollback()
        conn.close()

def delete_workout(log_id):
    conn = connect_db()
    if conn is None: return
    try:
        cursor = conn.cursor()
        query = "DELETE FROM workout_logs WHERE id = %s"
        cursor.execute(query, (log_id,))
        conn.commit()
    except Exception as e:
     print(f"ошибка при удалении: {e}")
     if conn:
        conn.rollback()
        conn.close()

def get_fitness_stats():
    conn = connect_db()
    if conn is None: return {}
    try:
        cursor = conn.cursor()
        stats = {}
        cursor.execute("SELECT COUNT(*) FROM workout_logs")
        stats['count'] = cursor.fetchone()[0]
        cursor.execute("SELECT SUM(weight * reps * sets) FROM workout_logs")
        tonnage = cursor.fetchone()[0]
        stats['total_tonnage'] = tonnage if tonnage else 0
        cursor.execute("SELECT AVG(weight) FROM workout_logs WHERE weight IS NOT NULL")
        avg = cursor.fetchone()[0]
        stats['avg_weight'] = round(avg, 1) if avg else 0
        cursor.execute("""
                 SELECT muscle, COUNT(*) as cnt
                 FROM workout_logs
                 GROUP BY muscle
                 ORDER BY cnt DESC
                 LIMIT 1
                        """)
        popular = cursor.fetchone()
        stats['popular_muscle'] = popular[0] if popular else 'Нет данных'
   
        return stats
    except Exception as e:
     print(f"ошибка при фильтрации: {e}")
     if conn:
        conn.close()
        return[]

def print_workouts(workouts):
    if not workouts:
        print('Пора начать тренироваться!')
        return
    for w in workouts:
        # Порядок: id, exercise_name, weight_kg, reps, sets, muscle_group, notes
        print(f"{w[1]} ({w[2]}) - {w[3]}кг x {w[4]} x {w[5]} | {w[6]}")

def main():
    while True:
        print('\n=== ДНЕВНИК СПОРТСМЕНА ===')
        print('1. Добавить тренировку')
        print('2. Показать все тренировки')
        print('3. Поиск по упражнению')
        print('4. Фильтр по группе мышц')
        print('5. Обновить тренировку')
        print('6. Удалить тренировку')
        print('7. Статистика')
        print('8. Выход')
        choice = input('Выберите пункт: ')

        if choice == '1':
            exercise = input('Упражнение: ')
            date = input('Дата (ГГГГ-ММ-ДД): ')
            weight = int(input('Вес (кг): '))
            reps = int(input('Повторения: '))
            sets = int(input('Подходы: '))
            muscle = input('Группа мышц (Грудь/Спина/Ноги/Руки/Плечи/Пресс): ')
            notes = input('Заметки: ')
            workout_id = add_workout(exercise, weight, reps, sets, muscle, notes)
            if workout_id:
                print(f'Тренировка добавлена с ID: {workout_id}')
        elif choice == '2':
            workouts = get_all_workouts()
            print_workouts(workouts)
        elif choice == '3':
            exercise = input('Название упражнения: ')
            workouts = search_by_exercise(exercise)
            print_workouts(workouts)
        elif choice == '4':
            muscle = input('Группа мышц: ')
            workouts = filter_by_muscle(muscle)
            print_workouts(workouts)
        elif choice == '5':
            log_id = int(input('ID тренировки: '))
            new_weight = int(input('Новый вес: '))
            new_notes = input('Новые заметки: ')
            update_workout(log_id, new_weight, new_notes)
            print('Обновлено')
        elif choice == '6':
            log_id = int(input('ID для удаления: '))
            delete_workout(log_id)
            print('Удалено')
        elif choice == '7':
            stats = get_fitness_stats()
            print(f"Всего тренировок: {stats.get('count', 0)}")
            print(f"Суммарный тоннаж: {stats.get('total_tonnage', 0)} кг")
            print(f"Средний вес: {stats.get('avg_weight', 0)} кг")
            print(f"Популярная группа: {stats.get('popular_muscle', 'Нет данных')}")
        elif choice == '8':
            break
        else:
            print('Неверный ввод')

if __name__ == '__main__':
    main()