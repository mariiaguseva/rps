import hashlib
import json
import mysql.connector
from mysql.connector import Error


class DatabaseManager:
    def __init__(self):
        self.host = 'localhost'
        self.database = 'sorting_app'
        self.user = 'root'
        self.password = '1234'

    #соединение с базой данных
    def get_connection(self):
        try:
            connection = mysql.connector.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password
            )
            return connection
        except Error:
            print(f"Ошибка подключения к MySQL: {Error}")
            return None

    #регистрация пользователя
    def register_user(self, username, password):
        connection = self.get_connection()
        if connection is None:
            return False, "Ошибка подключения к базе данных"
        try:
            cursor = connection.cursor()
            #хеширование пароля
            hashed_password = hashlib.sha256(password.encode()).hexdigest() #енкод в байты ша256 алгоритм преобразования, хекс строка
            cursor.execute(
                "INSERT INTO users (username, password) VALUES (%s, %s)",
                (username, hashed_password)
            )
            #фиксация изменений
            connection.commit()
            return True, "Пользователь успешно зарегистрирован"
        except Error:
            return False, f"Ошибка регистрации: {str(Error)}"
        finally:
            cursor.close()
            connection.close()

    #вход пользователя
    def authenticate_user(self, username, password):
        connection = self.get_connection()
        if connection is None:
            return False, "Ошибка подключения к базе данных"
        try:
            cursor = connection.cursor()
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            #выполнение запроса sql
            cursor.execute(
                "SELECT id, username FROM users WHERE username = %s AND password = %s",
                (username, hashed_password)
            )
            user = cursor.fetchone() #получение строки результата

            if user:
                return True, {"id": user[0], "username": user[1]}
            else:
                return False, "Неверное имя пользователя или пароль"
        except Error:
            return False, f"Ошибка аутентификации: {str(Error)}"
        finally:
            cursor.close()
            connection.close()

    #сохранение массива в бд
    def save_array(self, user_id, original_array, sorted_array):
        connection = self.get_connection()
        if connection is None:
            return False, "Ошибка подключения к базе данных"
        try:
            cursor = connection.cursor()
            #преобразуем массивы в JSON строки
            original_json = json.dumps(original_array)
            sorted_json = json.dumps(sorted_array)
            array_size = len(original_array)

            cursor.execute(
                """INSERT INTO arrays (user_id, original_array, sorted_array, array_size) 
                VALUES (%s, %s, %s, %s)""",
                (user_id, original_json, sorted_json, array_size)
            )
            connection.commit() #сохранение
            return True, "Массив успешно сохранен"
        except Error:
            return False, f"Ошибка сохранения: {str(Error)}"
        finally:
            cursor.close()
            connection.close()

    #считывание массивов
    def get_user_arrays(self, user_id):
        try:
            connection = self.get_connection()
            cursor = connection.cursor()
            cursor.execute("SELECT id, original_array, sorted_array, created_at FROM arrays WHERE user_id = %s",
                           (user_id,))
            rows = cursor.fetchall() #получение строк
            #преобразуем в список словарей
            arrays = []
            for row in rows:
                arrays.append({
                    'id': row[0],
                    'original_array': row[1],
                    'sorted_array': row[2],
                    'created_at': row[3]
                })

            return True, arrays

        except Exception:
            return False, f"Ошибка получения массивов: {str(Exception)}"
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

#создаем глобальный экземпляр менеджера БД
db_manager = DatabaseManager()