import sqlite3


DB_FILE = "traffic_data.db" # declare the sqlite db file name ( To be implemented in future iterations)



# ===================== function to create the database and table ===================== #

def create_database():

    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS traffic_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                pin_12 INTEGER NOT NULL,
                pin_7 INTEGER NOT NULL,
                pin_8 INTEGER NOT NULL
            )
        ''')


        conn.commit()
        print("Database and table created successfully.")


    except Exception as e:
        print(f"Error creating database: {e}")


def insert_data(timestamp, pin_12, pin_7, pin_8):

    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO traffic_data (timestamp, pin_12, pin_7, pin_8)
            VALUES (?, ?, ?, ?)
        ''', (timestamp, pin_12, pin_7, pin_8))

        conn.commit()
        print("Data inserted successfully.")


    except Exception as e:
        print(f"Error inserting data: {e}")


if __name__ == "__main__":
    create_database()