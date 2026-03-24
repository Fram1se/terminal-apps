import psycopg2
from datetime import datetime

def connect_db():
    try:
        conn = psycopg2.connect(
            dbname='movie_db',
            user='postgres',
            password='1111',
            host='localhost',
            port=5432
        )
        print('База фильмов подключена')
        return conn
    except Exception as e:
        print(f"Ошибка подключения: {e}")
        return None

def add_movie(title, duration, rating, genre, review):
    conn = connect_db()
    if conn is None:
        return None
    try:
        cursor = conn.cursor()
        query = """
            INSERT INTO movie_logs (title, duration_min, rating, genre, review)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(query, (title, duration, rating, genre, review))
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
     print(f"Ошибка при добавлении фильма: {e}")
     if conn:
        conn.rollback()
        conn.close()

def get_all_movies():
    conn = connect_db()
    if conn is None:
         return []
    try:
        cursor = conn.cursor()
        query = "SELECT * FROM movie_logs ORDER BY title DESC"
        cursor.execute(query)
        movies = cursor.fetchall()
        cursor.close() 
        conn.close()
        return movies
    except Exception as e:
        print(f"Ошибка при получении списка фильмов: {e}")
        if conn:
            conn.close()
            return []


def search_by_title(movie_title):
    conn = connect_db()
    if conn is None:
         return []
    try:
        cursor = conn.cursor()
        pattern = f"%{movie_title}%"
        query = "SELECT * FROM movie_logs WHERE title ILIKE %s ORDER BY title DESC"
        cursor.execute(query, (pattern,))
        movies = cursor.fetchall()
        cursor.close() 
        conn.close()
        return movies
    except Exception as e:
        print(f"Ошибка при поиске по названию: {e}")
        if conn:
            conn.close()
            return []


def filter_by_rating(min_rating):
    conn = connect_db()
    if conn is None:
        return []
    try:
        cursor = conn.cursor()
        query = "SELECT * FROM movie_logs WHERE rating >= %s ORDER BY rating DESC"
        cursor.execute(query, (min_rating,))
        movies = cursor.fetchall()
        cursor.close() 
        conn.close()
        return movies
    
    except Exception as e:
        print(f"Ошибка при фильтрации по рейтингу: {e}")
        if conn:
            conn.close()
            return []

def update_movie(log_id, new_rating, new_review):
    conn = connect_db()
    
    if conn is None:
        return

    try:
        cursor = conn.cursor()
    
        query = "UPDATE movie_logs SET rating = %s, review = %s WHERE id = %s"
        cursor.execute(query, (new_rating, new_review, log_id))
        conn.commit()
        cursor.close()
    
        conn.close()
    except Exception as e:
        print(f"Ошибка при обновлении фильма: {e}")
        if conn:
            conn.rollback()
            conn.close()

def delete_movie(log_id):
    conn = connect_db()
    if conn is None:
        return
    try:
        cursor = conn.cursor()
        query = "DELETE FROM movie_logs WHERE id = %s"
        cursor.execute(query, (log_id,))
        conn.commit()
        cursor.close() 
        conn.close()
    except Exception as e:
        print(f"Ошибка при удалении фильма: {e}")
        if conn:
            conn.rollback()
            conn.close()

def get_cinema_stats():
    
    conn = connect_db()
    
    if conn is None:
        return {}
    try:
        cursor = conn.cursor()
        stats = {}
        cursor.execute("SELECT COUNT(*) FROM movie_logs")
        stats['count'] = cursor.fetchone()[0]
    
        cursor.execute("SELECT AVG(rating) FROM movie_logs WHERE rating IS NOT NULL")
        avg = cursor.fetchone()[0]
        stats['avg_rating'] = round(avg, 1) if avg else 0
    
        cursor.execute("SELECT SUM(duration_min) FROM movie_logs")
        total_minutes = cursor.fetchone()[0]
        stats['total_hours'] = total_minutes // 60 if total_minutes else 0
    
    
        cursor.execute("""
                SELECT genre, COUNT(*) as cnt
               FROM movie_logs
               GROUP BY genre
               ORDER BY cnt DESC
               LIMIT 1
                """)
        popular = cursor.fetchone()
        stats['popular_genre'] = popular[0] if popular else 'Нет данных'
    
        cursor.close()
        conn.close()
        return stats
    
    except Exception as e:
        print(f"Ошибка при получении статистики: {e}")
        if conn:
            conn.close()
            return {}
    

def print_movies(movies):
    if not movies:
        print('Пора начать смотреть кино!')
        return
    for m in movies:
        # Предполагаемый порядок: id, title, watch_date, duration_min, rating, genre, review
        print(f"{m[1]} ({m[2]}) - Оценка: {m[4]}/10")

def main():
    while True:
        print('\n=== ДНЕВНИК КИНОМАНА ===')
        print('1. Добавить фильм')
        print('2. Показать все фильмы')
        print('3. Поиск по названию')
        print('4. Фильтр по рейтингу')
        print('5. Обновить фильм')
        print('6. Удалить фильм')
        print('7. Статистика')
        print('8. Выход')
        choice = input('Выберите пункт: ')

        if choice == '1':
            title = input('Название: ')
            duration = int(input('Длительность (мин): '))
            rating = int(input('Оценка (1-10): '))
            genre = input('Жанр (Боевик, Комедия, Драма, Фантастика, Другое): ')
            review = input('Отзыв: ')
            movie_id = add_movie(title, duration, rating, genre, review)
            if movie_id:
                print(f'Фильм добавлен с ID: {movie_id}')
        elif choice == '2':
            movies = get_all_movies()
            print_movies(movies)
        elif choice == '3':
            title = input('Название для поиска: ')
            movies = search_by_title(title)
            print_movies(movies)
        elif choice == '4':
            min_r = int(input('Минимальный рейтинг: '))
            movies = filter_by_rating(min_r)
            print_movies(movies)
        elif choice == '5':
            log_id = int(input('ID фильма: '))
            new_r = int(input('Новая оценка: '))
            new_rev = input('Новый отзыв: ')
            update_movie(log_id, new_r, new_rev)
            print('Обновлено')
        elif choice == '6':
            log_id = int(input('ID фильма для удаления: '))
            delete_movie(log_id)
            print('Удалено')
        elif choice == '7':
            stats = get_cinema_stats()
            print(f"Всего фильмов: {stats.get('count', 0)}")
            print(f"Средняя оценка: {stats.get('avg_rating', 0)}")
            print(f"Время в часах: {stats.get('total_hours', 0)}")
        elif choice == '8':
            break
        else:
            print('Неверный ввод')

if __name__ == '__main__':
    main()
