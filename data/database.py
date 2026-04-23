import sqlite3
import streamlit as st
from datetime import datetime
import json
import os

DATA_DIR = "data"
VENDEURS_FILE = os.path.join(DATA_DIR, "vendeurs.json")
ANNONCES_FILE = os.path.join(DATA_DIR, "annonces.json")

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

def ensure_data_dir():
    os.makedirs(DATA_DIR, exist_ok=True)

# =========================
# Gestion des vendeurs
# =========================
def load_vendeurs():
    ensure_data_dir()
    if not os.path.exists(VENDEURS_FILE):
        return []

    with open(VENDEURS_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_vendeurs(vendeurs):
    ensure_data_dir()
    with open(VENDEURS_FILE, "w", encoding="utf-8") as f:
        json.dump(vendeurs, f, ensure_ascii=False, indent=2)

def save_vendeur(vendeur: dict):
    vendeurs = load_vendeurs()
    vendeurs.append(vendeur)
    save_vendeurs(vendeurs)

def email_exists(email: str) -> bool:
    return any(v.get("email", "").lower() == email.lower() for v in load_vendeurs())

def get_vendeur_by_id(vendeur_id: str):
    vendeurs = load_vendeurs()
    for vendeur in vendeurs:
        if vendeur.get("id") == vendeur_id:
            return vendeur
    return None

# =========================
# Gestion des annonces
# =========================
def load_annonces():
    ensure_data_dir()
    if not os.path.exists(ANNONCES_FILE):
        return []

    with open(ANNONCES_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_annonces(annonces):
    ensure_data_dir()
    with open(ANNONCES_FILE, "w", encoding="utf-8") as f:
        json.dump(annonces, f, ensure_ascii=False, indent=2)

def save_annonce(annonce: dict):
    annonces = load_annonces()
    annonces.append(annonce)
    save_annonces(annonces)