import streamlit as st
import json
import os
import re
from datetime import datetime

# ── Configuration de la page ──────────────────────────────────────────────────
st.set_page_config(
    page_title="AgroSénégal — Créer mon profil",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Style CSS (cohérent avec app.py) ─────────────────────────────────────────
st.markdown("""
    <style>
        /* ---- palette identique à app.py ---- */
        :root {
            --green-dark:   #1B5E20;
            --green-mid:    #2E7D32;
            --green-light:  #388E3C;
            --green-pale:   #F1F8E9;
            --accent:       #66BB6A;
        }

        /* ---- titres ---- */
        .main-title {
            font-size: 2.4em;
            color: var(--green-dark);
            font-weight: bold;
            text-align: center;
        }
        .subtitle {
            font-size: 1.15em;
            color: var(--green-light);
            text-align: center;
        }

        /* ---- cartes de section ---- */
        .section-card {
            background-color: var(--green-pale);
            padding: 24px 28px;
            border-radius: 12px;
            border-left: 5px solid var(--green-mid);
            margin: 14px 0;
        }
        .section-card h3 {
            color: var(--green-dark);
            margin-bottom: 4px;
        }

        /* ---- badge de succès ---- */
        .success-box {
            background-color: #E8F5E9;
            border: 1px solid #A5D6A7;
            border-radius: 10px;
            padding: 18px 24px;
            text-align: center;
            color: var(--green-dark);
            font-size: 1.05em;
        }

        /* ---- étapes ---- */
        .step-indicator {
            display: flex;
            justify-content: center;
            gap: 12px;
            margin-bottom: 10px;
        }
        .step {
            background: #C8E6C9;
            color: var(--green-dark);
            border-radius: 20px;
            padding: 4px 16px;
            font-size: 0.85em;
            font-weight: 600;
        }
        .step.active {
            background: var(--green-mid);
            color: white;
        }

        /* ---- séparateur de section ---- */
        .section-title {
            color: var(--green-dark);
            font-weight: 700;
            font-size: 1.1em;
            border-bottom: 2px solid var(--accent);
            padding-bottom: 4px;
            margin-bottom: 12px;
        }
    </style>
""", unsafe_allow_html=True)

# ── Chemin du fichier de données ──────────────────────────────────────────────
DATA_DIR  = "data"
DATA_FILE = os.path.join(DATA_DIR, "vendeurs.json")

def load_vendeurs():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_vendeur(vendeur: dict):
    os.makedirs(DATA_DIR, exist_ok=True)
    vendeurs = load_vendeurs()
    vendeurs.append(vendeur)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(vendeurs, f, ensure_ascii=False, indent=2)

def email_exists(email: str) -> bool:
    return any(v.get("email", "").lower() == email.lower() for v in load_vendeurs())

def tel_valid(tel: str) -> bool:
    return bool(re.fullmatch(r"(\+221)?[37][0-9]{8}", tel.replace(" ", "")))

# ── En-tête ───────────────────────────────────────────────────────────────────
st.markdown('<p class="main-title">🧑‍🌾 Créer mon profil vendeur</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Rejoignez la communauté AgroSénégal et trouvez vos acheteurs à Dakar</p>', unsafe_allow_html=True)

st.divider()

# ── Indicateur d'étape ────────────────────────────────────────────────────────
st.markdown("""
<div class="step-indicator">
    <span class="step active">① Informations personnelles</span>
    <span class="step active">② Activité agricole</span>
    <span class="step active">③ Localisation</span>
    <span class="step active">④ Sécurité</span>
</div>
""", unsafe_allow_html=True)

st.write("")

# ── Formulaire principal ──────────────────────────────────────────────────────
with st.form("form_profil_vendeur", clear_on_submit=False):

    # ── Section 1 : Informations personnelles ─────────────────────────────────
    st.markdown('<div class="section-title">👤 Informations personnelles</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        prenom = st.text_input("Prénom *", placeholder="ex. Moussa")
        email  = st.text_input("Adresse e-mail *", placeholder="ex. moussa@gmail.com")
    with col2:
        nom    = st.text_input("Nom *", placeholder="ex. Diallo")
        tel    = st.text_input("Téléphone *", placeholder="ex. 77 123 45 67")

    photo_url = st.text_input(
        "Lien photo de profil (optionnel)",
        placeholder="https://... (lien vers votre photo)",
        help="Collez un lien public vers votre photo (Google Drive, Imgur, etc.)"
    )

    st.write("")

    # ── Section 2 : Activité agricole ─────────────────────────────────────────
    st.markdown('<div class="section-title">🌿 Activité agricole</div>', unsafe_allow_html=True)

    CATEGORIES = [
        "Légumes frais", "Fruits", "Céréales & grains",
        "Tubercules & racines", "Légumineuses", "Épices & condiments",
        "Produits transformés", "Volailles & œufs", "Autre"
    ]

    categories = st.multiselect(
        "Catégories de produits vendus *",
        options=CATEGORIES,
        help="Sélectionnez une ou plusieurs catégories"
    )

    col3, col4 = st.columns(2)
    with col3:
        experience = st.selectbox(
            "Années d'expérience",
            ["Moins d'1 an", "1 – 3 ans", "3 – 5 ans", "5 – 10 ans", "Plus de 10 ans"]
        )
    with col4:
        capacite = st.selectbox(
            "Capacité de production / semaine",
            ["Moins de 50 kg", "50 – 200 kg", "200 – 500 kg", "Plus de 500 kg"]
        )

    bio = st.checkbox("🌱 Je pratique l'agriculture biologique / naturelle")
    livraison = st.checkbox("🚚 Je propose la livraison")

    description = st.text_area(
        "Présentation de votre activité *",
        placeholder="Décrivez vos produits, votre façon de travailler, ce qui vous différencie...",
        height=110
    )

    st.write("")

    # ── Section 3 : Localisation ──────────────────────────────────────────────
    st.markdown('<div class="section-title">📍 Localisation</div>', unsafe_allow_html=True)

    COMMUNES = [
        "Dakar Plateau", "Médina", "Biscuiterie", "Grand-Dakar", "Hann Bel-Air",
        "Gueule Tapée-Fass-Colobane", "Parcelles Assainies", "Yeumbeul Nord",
        "Yeumbeul Sud", "Malika", "Pikine Nord", "Pikine Est", "Pikine Ouest",
        "Guédiawaye", "Ngor", "Ouakam", "Yoff", "Almadies", "Sacré-Cœur",
        "Point E", "Mermoz-Sacré-Cœur", "Liberté", "Grand-Yoff",
        "Dieuppeul-Derklé", "Cambérène", "Rufisque", "Sangalkam", "Autre"
    ]

    col5, col6 = st.columns(2)
    with col5:
        commune = st.selectbox("Commune / Quartier *", COMMUNES)
    with col6:
        marche = st.text_input("Marché habituel (optionnel)", placeholder="ex. Marché Sandaga, Tilène...")

    adresse = st.text_input(
        "Adresse ou point de repère *",
        placeholder="ex. Près de la grande mosquée de Pikine"
    )

    st.write("")

    # ── Section 4 : Sécurité ──────────────────────────────────────────────────
    st.markdown('<div class="section-title">🔒 Sécurité du compte</div>', unsafe_allow_html=True)

    col7, col8 = st.columns(2)
    with col7:
        mdp  = st.text_input("Mot de passe *", type="password", placeholder="Min. 6 caractères")
    with col8:
        mdp2 = st.text_input("Confirmer le mot de passe *", type="password")

    st.write("")

    # ── Conditions d'utilisation ──────────────────────────────────────────────
    cgu = st.checkbox("✅ J'accepte les conditions d'utilisation d'AgroSénégal *")

    st.write("")

    submitted = st.form_submit_button(
        "🌱 Créer mon profil vendeur",
        use_container_width=True,
        type="primary"
    )

# ── Traitement du formulaire ──────────────────────────────────────────────────
if submitted:
    errors = []

    # Validations
    if not prenom.strip():       errors.append("Le prénom est obligatoire.")
    if not nom.strip():          errors.append("Le nom est obligatoire.")
    if not email.strip():        errors.append("L'e-mail est obligatoire.")
    elif "@" not in email:       errors.append("L'adresse e-mail n'est pas valide.")
    elif email_exists(email):    errors.append("Un compte avec cet e-mail existe déjà.")
    if not tel.strip():          errors.append("Le téléphone est obligatoire.")
    elif not tel_valid(tel):     errors.append("Numéro de téléphone invalide (format sénégalais attendu).")
    if not categories:           errors.append("Sélectionnez au moins une catégorie de produits.")
    if not description.strip():  errors.append("La présentation de votre activité est obligatoire.")
    if not adresse.strip():      errors.append("L'adresse / point de repère est obligatoire.")
    if not mdp:                  errors.append("Le mot de passe est obligatoire.")
    elif len(mdp) < 6:           errors.append("Le mot de passe doit comporter au moins 6 caractères.")
    elif mdp != mdp2:            errors.append("Les mots de passe ne correspondent pas.")
    if not cgu:                  errors.append("Veuillez accepter les conditions d'utilisation.")

    if errors:
        for err in errors:
            st.error(f"⚠️ {err}")
    else:
        # Sauvegarde du profil
        vendeur = {
            "id":          datetime.now().strftime("%Y%m%d%H%M%S%f"),
            "prenom":      prenom.strip(),
            "nom":         nom.strip(),
            "email":       email.strip().lower(),
            "telephone":   tel.strip(),
            "photo_url":   photo_url.strip() if photo_url else "",
            "categories":  categories,
            "experience":  experience,
            "capacite":    capacite,
            "bio":         bio,
            "livraison":   livraison,
            "description": description.strip(),
            "commune":     commune,
            "marche":      marche.strip() if marche else "",
            "adresse":     adresse.strip(),
            "created_at":  datetime.now().isoformat(),
            "actif":       True
        }

        save_vendeur(vendeur)

        st.markdown(f"""
        <div class="success-box">
            🎉 <strong>Bienvenue, {prenom.strip()} !</strong><br>
            Votre profil vendeur a été créé avec succès sur AgroSénégal.<br>
            Vous pouvez maintenant publier vos premières annonces.
        </div>
        """, unsafe_allow_html=True)

        st.balloons()

        st.write("")
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("📢 Publier une annonce", use_container_width=True, type="primary"):
                st.switch_page("pages/02_annonce.py")
        with col_b:
            if st.button("🏠 Retour à l'accueil", use_container_width=True):
                st.switch_page("app.py")

st.divider()

# ── Footer identique à app.py ─────────────────────────────────────────────────
st.markdown("""
<div style="text-align: center; color: gray; font-size: 0.9em;">
    AgroSénégal © 2026 — Sprint 1 MVP | Développé avec ❤️ à Dakar
</div>
""", unsafe_allow_html=True)
