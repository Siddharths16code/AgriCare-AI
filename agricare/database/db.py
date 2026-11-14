
import sqlite3
from pathlib import Path

# -----------------------------------
# DATABASE CONFIGURATION
# -----------------------------------

DATABASE_PATH = (
    Path(__file__).resolve().parent / "agricare.db"
)


# -----------------------------------
# DATABASE CONNECTION
# -----------------------------------

def get_connection():

    connection = sqlite3.connect(DATABASE_PATH)

    connection.row_factory = sqlite3.Row

    connection.execute("PRAGMA foreign_keys = ON")

    return connection


# -----------------------------------
# INITIALIZE DATABASE
# -----------------------------------

def initialize_database():

    connection = get_connection()

    cursor = connection.cursor()

    # 1. FARMER USERS
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            phone TEXT UNIQUE,
            password_hash TEXT NOT NULL,
            village TEXT,
            district TEXT,
            state TEXT,
            preferred_language TEXT DEFAULT 'English',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # 2. FARM DETAILS
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS farms (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            farm_name TEXT NOT NULL,
            area_acres REAL,
            soil_type TEXT,
            irrigation_method TEXT,
            potato_variety TEXT,
            sowing_date TEXT,
            crop_stage TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY (user_id)
            REFERENCES users(id)
            ON DELETE CASCADE
        )
    """)

    # 3. DISEASE SCANS
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS scans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            farm_id INTEGER,
            image_path TEXT,
            predicted_class TEXT NOT NULL,
            confidence REAL,
            probabilities_json TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY (user_id)
            REFERENCES users(id)
            ON DELETE CASCADE,

            FOREIGN KEY (farm_id)
            REFERENCES farms(id)
            ON DELETE SET NULL
        )
    """)

    # 4. FARM ACTIVITIES
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS activities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            farm_id INTEGER,
            activity_name TEXT NOT NULL,
            description TEXT,
            scheduled_date TEXT,
            status TEXT DEFAULT 'Pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY (user_id)
            REFERENCES users(id)
            ON DELETE CASCADE,

            FOREIGN KEY (farm_id)
            REFERENCES farms(id)
            ON DELETE SET NULL
        )
    """)

    # 5. FARM EXPENSES
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            farm_id INTEGER,
            category TEXT NOT NULL,
            amount REAL NOT NULL,
            description TEXT,
            expense_date TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY (user_id)
            REFERENCES users(id)
            ON DELETE CASCADE,

            FOREIGN KEY (farm_id)
            REFERENCES farms(id)
            ON DELETE SET NULL
        )
    """)

    # 6. HARVEST RECORDS
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS harvest_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            farm_id INTEGER,
            harvest_date TEXT,
            quantity_kg REAL,
            selling_price REAL,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY (user_id)
            REFERENCES users(id)
            ON DELETE CASCADE,

            FOREIGN KEY (farm_id)
            REFERENCES farms(id)
            ON DELETE SET NULL
        )
    """)

    # INDEXES FOR FASTER QUERIES
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_farms_user
        ON farms(user_id)
    """)

    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_scans_user
        ON scans(user_id)
    """)

    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_activities_user
        ON activities(user_id)
    """)

    connection.commit()
    connection.close()


# -----------------------------------
# DATABASE VERIFICATION
# -----------------------------------

if __name__ == "__main__":

    initialize_database()

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        SELECT name
        FROM sqlite_master
        WHERE type = 'table'
        AND name NOT LIKE 'sqlite_%'
        ORDER BY name
    """)

    tables = cursor.fetchall()

    print("\nAgriCare AI Database Initialized!")
    print("--------------------------------")

    for table in tables:
        print("Table:", table["name"])

    connection.close()

    print("\nDatabase location:")
    print(DATABASE_PATH)


if __name__ == "__main__":

    initialize_database()

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        SELECT name
        FROM sqlite_master
        WHERE type = 'table'
        AND name NOT LIKE 'sqlite_%'
        ORDER BY name
    """)

    tables = cursor.fetchall()

    print("\nAgriCare AI Database Initialized!")
    print("--------------------------------")

    for table in tables:
        print("Table:", table["name"])

    connection.close()

    print("\nDatabase location:")
    print(DATABASE_PATH)