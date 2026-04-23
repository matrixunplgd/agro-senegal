import streamlit as st
import re
from datetime import datetime
from data.database import save_vendeur, email_exists

st.set_page_config(
    page_title="AgroSénégal — Créer mon profil",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
        :root { --green-dark: #1B5E20; --green-mid: #2E7D32; --green-light: #388E3C; --accent: #66BB6A; }
        .main-title { font-size: 2.4em; color: var(--green-dark); font-weight: bold; text-align: center; }
        .subtitle { font-size: 1.15em; color: var(--green-light); text-align: center; }
        .section-card { background-color: #F1F8E9; padding: 24px 28px; border-radius: 12px; border-left: 5px solid var(--green-mid); margin: 14px 0; }
        .success-box { background-color: #E8F5E9; border: 1px solid #A5D6A7; border-radius: 10px; padding: 18px 24px; text-align: center; color: var(--green-dark); }
        .step-indicator { display: flex; justify-content: center; gap: 12px; margin-bottom: 10px; }
        .step { background: #C8E6C9; color: var(--green-dark); border-radius: 20px; padding: 4px 16px; font-size: 0.85em; font-weight: 600; }
        .step.active { background: var(--green-mid); color: white; }
        .section-title { color: var(--green-dark); font-weight: 700; font-size: 1.1em; border-bottom: 2px solid var(--accent); padding-bottom: 4px; margin-bottom: 12px; }
    </style>
""", unsafe_allow_html=True)

def tel_valid(tel: str) -> bool:
    return bool(re.fullmatch(r"(\+221)?[37][0-9]{8}", tel.replace(" ", "")))

st.markdown('<p class="main-title">🧑‍🌾 Créer mon profil vendeur</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Rejoignez la communauté AgroSénégal et trouvez vos acheteurs à Dakar</p>', unsafe_allow_html=True)
st.divider()

st.markdown("""
<div class="step-indicator">
    <span class="step active">① Informations personnelles</span>
    <span class="step active">② Activité agricole</span>
    <span class="step active">③ Localisation</span>
    <span class="step active">④ Sécurité</span>
</div>
""", unsafe_allow_html=True)

with st.form("form_profil_vendeur", clear_on_submit=False):
    st.markdown('<div class="section-title">👤 Informations personnelles</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        prenom = st.text_input("Prénom *", placeholder="ex. Moussa")
        email  = st.text_input("Adresse e-mail *", placeholder="ex. moussa@gmail.com")
    with col2:
        nom    = st.text_input("Nom *", placeholder="ex. Diallo")
        tel    = st.text_input("Téléphone *", placeholder="ex. 77 123 45 67")
    photo_url = st.text_input("Lien photo de profil (optionnel)", placeholder="https://...")

    st.markdown('<div class="section-title">🌿 Activité agricole</div>', unsafe_allow_html=True)
    CATEGORIES = ["Légumes frais", "Fruits", "Céréales & grains", "Tubercules & racines", "Légumineuses", "Épices & condiments", "Produits transformés", "Volailles & œufs", "Autre"]
    categories = st.multiselect("Catégories de produits vendus *", options=CATEGORIES)
    col3, col4 = st.columns(2)
    with col3:
        experience = st.selectbox("Années d'expérience", ["Moins d'1 an", "1 – 3 ans", "3 – 5 ans", "5 – 10 ans", "Plus de 10 ans"])
    with col4:
        capacite = st.selectbox("Capacité de production / semaine", ["Moins de 50 kg", "50 – 200 kg", "200 – 500 kg", "Plus de 500 kg"])
    bio = st.checkbox("🌱 Je pratique l'agriculture biologique / naturelle")
    livraison = st.checkbox("🚚 Je propose la livraison")
    description = st.text_area("Présentation de votre activité *", height=110)

    st.markdown('<div class="section-title">📍 Localisation</div>', unsafe_allow_html=True)
    COMMUNES = ["Dakar Plateau", "Médina", "Biscuiterie", "Grand-Dakar", "Hann Bel-Air", "Gueule Tapée-Fass-Colobane", "Parcelles Assainies", "Yeumbeul Nord", "Yeumbeul Sud", "Malika", "Pikine Nord", "Pikine Est", "Pikine Ouest", "Guédiawaye", "Ngor", "Ouakam", "Yoff", "Almadies", "Sacré-Cœur", "Point E", "Mermoz-Sacré-Cœur", "Liberté", "Grand-Yoff", "Dieuppeul-Derklé", "Cambérène", "Rufisque", "Sangalkam", "Autre"]
    col5, col6 = st.columns(2)
    with col5:
        commune = st.selectbox("Commune / Quartier *", COMMUNES)
    with col6:
        marche = st.text_input("Marché habituel (optionnel)")
    adresse = st.text_input("Adresse ou point de repère *")

    st.markdown('<div class="section-title">🔒 Sécurité du compte</div>', unsafe_allow_html=True)
    col7, col8 = st.columns(2)
    with col7:
        mdp  = st.text_input("Mot de passe *", type="password", placeholder="Min. 6 caractères")
    with col8:
        mdp2 = st.text_input("Confirmer le mot de passe *", type="password")
    cgu = st.checkbox("✅ J'accepte les conditions d'utilisation d'AgroSénégal *")
    submitted = st.form_submit_button("🌱 Créer mon profil vendeur", use_container_width=True, type="primary")

if submitted:
    errors = []
    if not prenom.strip(): errors.append("Prénom obligatoire.")
    if not nom.strip(): errors.append("Nom obligatoire.")
    if not email.strip(): errors.append("E-mail obligatoire.")
    elif "@" not in email: errors.append("E-mail invalide.")
    elif email_exists(email): errors.append("E-mail déjà utilisé.")
    if not tel.strip(): errors.append("Téléphone obligatoire.")
    elif not tel_valid(tel): errors.append("Numéro invalide (format sénégalais).")
    if not categories: errors.append("Au moins une catégorie.")
    if not description.strip(): errors.append("Description obligatoire.")
    if not adresse.strip(): errors.append("Adresse obligatoire.")
    if not mdp: errors.append("Mot de passe obligatoire.")
    elif len(mdp) < 6: errors.append("Mot de passe ≥ 6 caractères.")
    elif mdp != mdp2: errors.append("Mots de passe différents.")
    if not cgu: errors.append("Acceptez les conditions.")

    if errors:
        for err in errors:
            st.error(f"⚠️ {err}")
    else:
        vendeur_id = datetime.now().strftime("%Y%m%d%H%M%S%f")
        vendeur = {
            "id": vendeur_id,
            "prenom": prenom.strip(),
            "nom": nom.strip(),
            "email": email.strip().lower(),
            "telephone": tel.strip(),
            "mot_de_passe": mdp,
            "photo_url": photo_url.strip() if photo_url else "",
            "categories": categories,
            "experience": experience,
            "capacite": capacite,
            "bio": bio,
            "livraison": livraison,
            "description": description.strip(),
            "commune": commune,
            "marche": marche.strip() if marche else "",
            "adresse": adresse.strip(),
            "created_at": datetime.now().isoformat(),
            "actif": True
        }
        save_vendeur(vendeur)

        # Connexion automatique
        st.session_state["vendeur_id"] = vendeur_id
        st.session_state["vendeur_nom"] = f"{prenom.strip()} {nom.strip()}"
        st.session_state["vendeur_email"] = email.strip().lower()
        st.session_state["vendeur_phone"] = tel.strip()
        st.session_state["token"] = "ok"
        st.session_state["nom"] = f"{prenom.strip()} {nom.strip()}"
        st.session_state["quartier"] = commune

        st.markdown(f"""
        <div class="success-box">
            🎉 <strong>Bienvenue, {prenom.strip()} !</strong><br>
            Votre profil vendeur a été créé avec succès.<br>
            Vous êtes maintenant connecté automatiquement.
        </div>
        """, unsafe_allow_html=True)
        st.balloons()
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("📢 Publier une annonce", key="publish_after_profil", use_container_width=True):
                st.switch_page("pages/02_annonce.py")
        with col_b:
            if st.button("📊 Tableau de bord", key="dashboard_after_profil", use_container_width=True):
                st.switch_page("pages/03_dashboard.py")

st.divider()
st.markdown("""
<div style="text-align: center; color: gray; font-size: 0.9em;">
    AgroSénégal © 2026 — Sprint 1 MVP | Développé avec ❤️ à Dakar
</div>
""", unsafe_allow_html=True)