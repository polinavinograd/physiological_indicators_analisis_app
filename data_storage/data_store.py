import os
from datetime import datetime, date, time
import sqlite3
import pandas as pd
from path import LOCAL_PATH


class IndicatorsDataStorage:
    def __init__(self, db_path=os.path.join(LOCAL_PATH, "/data_storage/indicators_database.db")):
        self.db_connection = sqlite3.connect(db_path, check_same_thread=False)
        self.cursor = self.db_connection.cursor()
        table_names = ["Ingredients", "Exercises", "UserStress", "UserFoodIntake", "UserTraining", "UserMenstruation"]
        for table_name in table_names:
            if self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?;",
                                       (table_name, )).fetchone() is None:
                self.initialize_db()

    def initialize_db(self) -> None:
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Ingredients (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ingredient CHAR,
                calories INTEGER
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Exercises (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name CHAR,
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
                calories_consumed INTEGER,
                date DATE
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS UserTraining (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id CHAR,
                calories_burned INTEGER,
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
                SELECT stress_level
                FROM Stress
                WHERE user_id = ? AND date = ?
            """
        self.cursor.execute(query, (user_id, current_date))
        return [row[0] for row in self.cursor.fetchall()]



    def load_data_from_xlsx(self, xlsx_file: str) -> None:
        df = pd.read_excel(os.path.join(LOCAL_PATH, "excel_db", xlsx_file), parse_dates=True)

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

    def insert_data(self, df: pd.DataFrame, table_name: str) -> None:
        df.to_sql(table_name, self.db_connection, index=False, if_exists='replace')

    def close_connection(self) -> None:
        self.db_connection.close()
