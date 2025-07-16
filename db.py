import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()
DB_URL = os.getenv("DATABASE_URL")

def log_interaction(question, answer):
    try:
        conn = psycopg2.connect(DB_URL)
        cur = conn.cursor()
        cur.execute("INSERT INTO interactions (question, answer) VALUES (%s, %s)", (question, answer))
        conn.commit()
    except Exception as e:
        print(f"Error logging interaction: {e}")
    finally:
        cur.close()
        conn.close()
