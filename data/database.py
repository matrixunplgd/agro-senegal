import json
import os

DATA_DIR = "data"
VENDEURS_FILE = os.path.join(DATA_DIR, "vendeurs.json")
ANNONCES_FILE = os.path.join(DATA_DIR, "annonces.json")

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
    for vendeur in load_vendeurs():
        if vendeur.get("id") == vendeur_id:
            return vendeur
    return None

def get_vendeur_by_phone(phone: str):
    phone_clean = phone.replace(" ", "").replace("-", "")
    for v in load_vendeurs():
        if v.get("telephone", "").replace(" ", "").replace("-", "") == phone_clean:
            return v
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

def get_annonces_by_vendeur(vendeur_id: str):
    return [a for a in load_annonces() if a.get("vendeur_id") == vendeur_id]

def update_annonce(annonce_id: str, updated_data: dict):
    annonces = load_annonces()
    for i, a in enumerate(annonces):
        if a.get("id") == annonce_id:
            annonces[i].update(updated_data)
            save_annonces(annonces)
            return True
    return False

def delete_annonce(annonce_id: str):
    annonces = load_annonces()
    for i, a in enumerate(annonces):
        if a.get("id") == annonce_id:
            del annonces[i]
            save_annonces(annonces)
            return True
    return False