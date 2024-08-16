import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv
import os

load_dotenv()

# -- Database Configurations --
conn = psycopg2.connect(
    dbname= os.environ.get('DB_NAME'),
    user= os.environ.get('DB_USER'),
    password= os.environ.get('DB_PASSWORD'),
    host= os.environ.get('DB_HOST'),
    port= os.environ.get('DB_PORT')
)
cursor = conn.cursor()

# -- Database Tables -- 

# Comments Table
def comments_table():
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS comments_data (
        id SERIAL PRIMARY KEY,
        video_id VARCHAR(255) NOT NULL,
        author VARCHAR(255),
        published_at TIMESTAMP,
        updated_at TIMESTAMP,
        like_count INTEGER,
        text TEXT,
        UNIQUE (video_id, author, published_at)
    )
    """)
    conn.commit()
    print('Comments table created or updated')
    
# Channels Table
def channels_table():
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS channels_data (
        id SERIAL PRIMARY KEY,
        channel_id VARCHAR(255) UNIQUE NOT NULL,
        title TEXT,
        description TEXT,
        view_count INTEGER,
        subscriber_count INTEGER,
        video_count INTEGER,
        published_at TIMESTAMP WITH TIME ZONE
    )
    """)
    conn.commit()
    print('Channels table created or updated')

def ensure_tables_exist():
    comments_table()
    channels_table()

ensure_tables_exist()