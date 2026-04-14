import sqlite3
import streamlit as st
from datetime import datetime

def init_db():
    conn = sqlite3.connect('data/profiles.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS profiles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT UNIQUE NOT NULL,
            location TEXT NOT NULL,
            market TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def add_profile(name, phone, location, market):
    conn = sqlite3.connect('data/profiles.db')
    c = conn.cursor()
    try:
        c.execute("INSERT INTO profiles (name, phone, location, market) VALUES (?, ?, ?, ?)", (name, phone, location, market))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def get_profiles():
    conn = sqlite3.connect('data/profiles.db')
    c = conn.cursor()
    c.execute("SELECT * FROM profiles ORDER BY created_at DESC")
    profiles = c.fetchall()
    conn.close()
    return [{'id': r[0], 'name': r[1], 'phone': r[2], 'location': r[3], 'market': r[4], 'photo': f"https://via.placeholder.com/200x200/2E7D32/FFFFFF?text={r[1][0]}", 'rating': 4.5, 'annonces': []} for r in profiles]
