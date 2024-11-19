import os
import psycopg2
from dotenv import load_dotenv

# Load environment variables
load_dotenv()  # Assumes .env is in the project root
DATABASE_URL = os.getenv("DATABASE_URL")

def query_logs():
    """Query logs from the database."""
    try:
        # Connect to the PostgreSQL database
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()

        # Example query: Fetch all logs
        cursor.execute("SELECT * FROM logs;")
        rows = cursor.fetchall()

        # Print the results
        for row in rows:
            print(row)

    except Exception as e:
        print(f"Error querying the database: {e}")
    finally:
        # Ensure the connection is closed
        if conn:
            cursor.close()
            conn.close()

if __name__ == "__main__":
    query_logs()
