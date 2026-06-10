import sqlite3
import asyncio

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
        with sqlite3.connect(DB_FILE) as conn:
            cursor = conn.cursor()

            cursor.execute('''
                INSERT INTO traffic_data (timestamp, pin_12, pin_7, pin_8)
                VALUES (?, ?, ?, ?)
            ''', (timestamp, pin_12, pin_7, pin_8))

            conn.commit()
            print("Data inserted successfully.")


    except Exception as e:
        print(f"Error inserting data: {e}")


def print_all_data():

    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM traffic_data')
        rows = cursor.fetchall()

        for row in rows:
            return (f"ID: {row[0]}, Timestamp: {row[1]}, Pin 12: {row[2]}, Pin 7: {row[3]}, Pin 8: {row[4]}")


    except Exception as e:
        print(f"Error retrieving data: {e}")


def blocking_get_all_data():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    try:
        cursor.execute('SELECT * FROM traffic_data')
        rows = cursor.fetchall()
        return rows
    except Exception as e:
        print(f"Error retrieving data: {e}")
        return []
    finally:
        conn.close()

def get_red_light_count():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    try:
        cursor.execute('SELECT COUNT(*) FROM traffic_data WHERE pin_12 = 1')
        count = cursor.fetchone()[0]
        print(f"Red light count: {count}")
        return count
    except Exception as e:
        print(f"Error retrieving red light count: {e}")
        return 0
    finally:
        conn.close()


async def get_all_data():
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, blocking_get_all_data)



    

        


if __name__ == "__main__":
    create_database()
    print_all_data()
    get_red_light_count()