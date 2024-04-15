from dotenv import load_dotenv
import os
import psycopg2



load_dotenv()

# Database configuration
DB_NAME = 'defaultdb'
DB_USER = 'admin'
DB_PASSWORD = os.environ.get('DB_PASSWORD')
DB_HOST = "typically-powerful-falcon-iad.a1.pgedge.io"
DB_PORT = "5432"

class DatabaseManager:
    def __init__(self):
        self.conn = self.connect_to_database()

    def connect_to_database(self):
        try:
            conn = psycopg2.connect(
                database=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD,
                host=DB_HOST,
                port=DB_PORT
            )
            print("Connected to database successfully!")
            return conn
        except psycopg2.Error as e:
            print("Unable to connect to the database:", e)
            exit(1)
            
    def insert_score(self, player_name, score):
        try:
            cursor = self.conn.cursor()
            cursor.execute("INSERT INTO scores (player_name, score) VALUES (%s, %s)", (player_name, score))
            self.conn.commit()
            cursor.close()
            print("Score inserted successfully!")
        except psycopg2.Error as e:
            print("Unable to insert score:", e)

    def fetch_leaderboard_data(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT player_name, score FROM scores WHERE player_name != '' ORDER BY score DESC LIMIT 10;")
            leaderboard_data = cursor.fetchall()
            cursor.close()
            return leaderboard_data
        except psycopg2.Error as e:
            print("Unable to fetch leaderboard data:", e)

