import os
from datetime import date, time
import sqlite3
import pandas as pd
from model.user import User

from path import LOCAL_PATH


class IndicatorsDataStorage:
    def __init__(self, db_path=os.path.join(LOCAL_PATH, "data_storage/indicators_database.db")):
        self.db_connection = sqlite3.connect(db_path, check_same_thread=False)
        self.cursor = self.db_connection.cursor()
        table_names = ["Ingredients", "Exercises", "UserStress", "UserFoodIntake", "UserTraining", "UserMenstruation",
                       "Users"]
        if len(self.cursor.execute("SELECT * "
                                   "FROM sqlite_master "
                                   "WHERE type='table' AND name NOT LIKE 'sqlite_%';").fetchall()) < 7:
            self.__initialize_db()
            for table_name in table_names:
                self.__load_data_from_xlsx(table_name + ".xlsx")
        print("\033[91mDataStorage created! \033[0m")

    def __initialize_db(self) -> None:
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Users (
                user_id CHAR PRIMARY KEY,
                weight INTEGER,
                height INTEGER,
                age INTEGER,
                brm FLOAT
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Ingredients (
                ingredient CHAR PRIMARY KEY,
                calories INTEGER
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Exercises (
                name CHAR PRIMARY KEY,
                calories INTEGER
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS UserStress (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id CHAR,
                stress_level INTEGER,
                date DATE,
                time TIME
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS UserFoodIntake (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id CHAR,
                calories INTEGER,
                date DATE
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS UserTraining (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id CHAR,
                calories INTEGER,
                date DATE
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS UserMenstruation (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id CHAR,
                abdominal_pain BOOLEAN,
                digestive_disorders BOOLEAN,
                breast_pain BOOLEAN,
                skin_rash BOOLEAN,
                mood INTEGER,
                menstruation_status BOOLEAN,
                date DATE
            )
        ''')

    def get_stress_by_day(self, user_id: str, current_date: date) -> list[int]:
        query = f"""
                SELECT IFNULL(stress_level, 0)
                FROM UserStress
                WHERE user_id = ? AND date = ?
            """
        self.cursor.execute(query, (user_id, current_date))
        return [row[0] for row in self.cursor.fetchall()]

    def get_calories_by_ingredient(self, ingredient_name: str):
        query = f"""
                SELECT calories
                FROM Ingredients
                WHERE ingredient = ?
            """
        self.cursor.execute(query, (ingredient_name,))
        return self.cursor.fetchone()[0]

    def get_calories_by_exercise(self, exercise_name: str):
        query = f"""
                SELECT calories
                FROM Exercises
                WHERE name = ?
            """
        self.cursor.execute(query, (exercise_name,))
        return self.cursor.fetchone()[0]

    def get_food_intake_by_day(self, user_id: str, current_date: date) -> int:
        query = f"""
                SELECT IFNULL(calories, 0)
                FROM UserFoodIntake
                WHERE user_id = ? AND date = ?
            """
        self.cursor.execute(query, (user_id, current_date))
        # result = self.cursor.fetchone() # TODO: А если это первый запрос за день?
        # return result[0]
        data = self.cursor.fetchone()
        if data == None or len(data) == 0:
            return 0

        return data[0]

    def get_calories_burned_by_day(self, user_id: str, current_date: str) -> int:
        query = f"""
                SELECT IFNULL(calories, 0)
                FROM UserTraining
                WHERE user_id = ? AND date = ?
            """
        print(user_id)
        print(current_date)
        self.cursor.execute(query, (user_id, current_date))

        data = self.cursor.fetchone()
        if data == None or len(data) == 0:
            return 0

        return data[0]

    def get_menstual_info(self, user_id: str):
        query = f"""
                SELECT *
                FROM UserMenstruation
                WHERE user_id = ?
            """
        self.cursor.execute(query, (user_id,))
        return self.cursor.fetchall()

    def __load_data_from_xlsx(self, xlsx_file: str) -> None:
        df = pd.read_excel(os.path.join(LOCAL_PATH, "data_storage/excel_db", xlsx_file), parse_dates=True)

        for column in df.columns:
            if pd.api.types.is_string_dtype(df[column]):
                df[column] = df[column].astype(str)
            elif pd.api.types.is_numeric_dtype(df[column]):
                df[column] = df[column].astype(int)
            elif pd.api.types.is_datetime64_any_dtype(df[column]):
                if df[column].dt.time.max() == time(0, 0):
                    df[column] = df[column].dt.date
                else:
                    df[column] = df[column].dt.time
        df.to_sql(xlsx_file[:-5], self.db_connection, index=False, if_exists='replace')
        self.db_connection.commit()

    def try_insert_user(self, data: dict) -> bool:
        user_id = data.get('user_id')
        if not self.__user_exists(user_id):
            columns = ', '.join(data.keys())
            values = ', '.join('?' for _ in data.values())
            query = f"INSERT INTO Users ({columns}) VALUES ({values})"
            try:
                self.cursor.execute(query, tuple(data.values()))
                self.db_connection.commit()
                return True
            except sqlite3.Error as e:
                print(f"Ошибка при вставке данных: {e}")
                return False
        else:
            query = 'UPDATE Users SET weight = ?, height = ?, age = ?, brm = ? WHERE user_id = ?'
            self.cursor.execute(query, (data['weight'], data['height'], data['age'], data['brm'], data['user_id']))
            self.db_connection.commit()
            return True

    def get_ingredients_list(self):
        query = 'SELECT * FROM Ingredients'
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def get_exercises_list(self):
        query = 'SELECT * FROM Exercises'
        self.cursor.execute(query)
        return self.cursor.fetchall()
    
    def get_user(self, user_id: str) -> User:
        get_query = "SELECT * FROM Users WHERE user_id = ?"
        try:
            self.cursor.execute(get_query, (user_id,))
            existing_data = self.cursor.fetchone()
            return User(
                user_id=existing_data[0],
                weight=existing_data[1],
                height=existing_data[2],
                age=existing_data[3],
                sex=False,
                brm=existing_data[4])

        except sqlite3.Error as e:
            print(f"Ошибка при извлечении пользователя: {e}")
            return False

    def __user_exists(self, user_id: str) -> bool:
        existing_query = "SELECT 1 FROM Users WHERE user_id = ?"
        try:
            self.cursor.execute(existing_query, (user_id,))
            existing_data = self.cursor.fetchone()
            return bool(existing_data)

        except sqlite3.Error as e:
            print(f"Ошибка при проверке наличия пользователя: {e}")
            return False

    def try_insert_calories(self, data: dict, table_name: str):
        existing_query = f"SELECT 1 FROM {table_name} WHERE user_id = ? AND date = ?"
        user_id, current_date, calories = data.get('user_id'), data.get('date'), data.get('calories')
        try:
            self.cursor.execute(existing_query, (user_id, current_date))
            existing_data = self.cursor.fetchone()

            if existing_data:
                self.cursor.execute(f"UPDATE {table_name} SET calories = ? WHERE user_id = ? AND date = ?",
                                    (calories, user_id, current_date))
                self.db_connection.commit()
            else:
                columns = ', '.join(data.keys())
                placeholders = ', '.join('?' for _ in data.values())
                if table_name == "UserTraining":
                    data['calories'] += 1500
                self.cursor.execute(f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})",
                                    tuple(data.values()))
                self.db_connection.commit()
            return True

        except sqlite3.Error as e:
            print(f"Ошибка при вставке или обновлении данных: {e}")
            return False

    def insert_stress_data(self, data: dict):
        columns = ', '.join(data.keys())
        values = ', '.join('?' for _ in data.values())
        query = f"INSERT INTO UserStress ({columns}) VALUES ({values})"
        self.cursor.execute(query, tuple(data.values()))
        self.db_connection.commit()

    def insert_menstruation_data(self, data: dict):
        existing_query = f"SELECT 1 FROM UserMenstruation WHERE user_id = ? AND date = ?"
        user_id, current_date = data.get('user_id'), data.get('date')
        try:
            self.cursor.execute(existing_query, (user_id, current_date))
            existing_data = self.cursor.fetchone()

            if existing_data:
                for key in data.keys():
                    self.cursor.execute(f"UPDATE UserMenstruation SET {key} = ? WHERE user_id = ? AND date = ?",
                                        (data[key], user_id, current_date))
                    self.db_connection.commit()
            else:
                columns = ', '.join(data.keys())
                placeholders = ', '.join('?' for _ in data.values())
                self.cursor.execute(f"INSERT INTO UserMenstruation ({columns}) VALUES ({placeholders})",
                                    tuple(data.values()))
                self.db_connection.commit()
            return True

        except sqlite3.Error as e:
            print(f"Ошибка при вставке или обновлении данных: {e}")
            return False

    def close_connection(self) -> None:
        self.db_connection.close()
