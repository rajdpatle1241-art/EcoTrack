
import sqlite3
import pandas as pd

DB_NAME = "energy.db"


def create_database():

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS buildings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            building_name TEXT UNIQUE,
            consumption REAL,
            monthly_limit REAL
        )
    """)

    cursor.execute("SELECT COUNT(*) FROM buildings")

    if cursor.fetchone()[0] == 0:

        buildings = [
            ("Academic Block", 2800, 2500),
            ("Library", 1600, 2000),
            ("Computer Lab", 2200, 2000),
            ("Hostel A", 1900, 2200),
            ("Hostel B", 1400, 1800),
            ("Administration", 900, 1200),
            ("Cafeteria", 850, 1000),
            ("Auditorium", 800, 1000)
        ]

        cursor.executemany("""
            INSERT INTO buildings
            (building_name, consumption, monthly_limit)
            VALUES (?, ?, ?)
        """, buildings)

    conn.commit()
    conn.close()


def get_buildings():

    conn = sqlite3.connect(DB_NAME)

    data = pd.read_sql_query(
        "SELECT * FROM buildings",
        conn
    )

    conn.close()

    return data


create_database()
