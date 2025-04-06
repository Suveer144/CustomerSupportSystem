import sqlite3
import pandas as pd

def create_connection(db_file):
    """Create a database connection to the SQLite database."""
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as e:
        print(e)
    return conn

def create_table(conn):
    """Create the tickets table."""
    try:
        cursor = conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS tickets (
            ticket_id TEXT PRIMARY KEY,
            issue_category TEXT,
            sentiment TEXT,
            priority TEXT,
            solution TEXT,
            resolution_status TEXT,
            date_of_resolution TEXT
        )
        ''')
        conn.commit()
    except sqlite3.Error as e:
        print(e)

def populate_table(conn, data_file):
    """Populate the tickets table with data from a CSV file."""
    try:
        df = pd.read_csv(data_file)
        df.to_sql('tickets', conn, if_exists='replace', index=False)
        conn.commit()
    except Exception as e:
        print(f"Error populating table: {e}")

if __name__ == '__main__':
    db_file = 'db/ticket_data.db'  # Relative path to the database
    conn = create_connection(db_file)
    if conn is not None:
        create_table(conn)
        populate_table(conn, 'data/Historical_ticket_data.csv')  # Relative path to the CSV file
        conn.close()
    else:
        print("Error! cannot create database connection.")