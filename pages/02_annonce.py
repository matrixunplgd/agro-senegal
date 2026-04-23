import streamlit as st
import os
from uuid import uuid4
from datetime import datetime
from data.database import save_annonce

st.set_page_config(
    page_title="AgroSénégal — Publier une annonce",
    page_icon="📢",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
        :root { --green-dark: #1B5E20; --green-mid: #2E7D32; --green-light: #388E3C; --accent: #66BB6A; }
        .main-title { font-size: 2.4em; color: var(--green-dark); font-weight: bold; text-align: center; }
        .subtitle { font-size: 1.15em; color: var(--green-light); text-align: center; }
        .section-title { color: var(--green-dark); font-weight: 700; border-bottom: 2px solid var(--accent); padding-bottom: 4px; margin-bottom: 12px; }
        .success-box { background-color: #E8F5E9; border: 1px solid #A5D6A7; border-radius: 10px; padding: 18px 24px; text-align: center; }
    </style>
""", unsafe_allow_html=True)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

st.markdown('<p class="main-title">📢 Publier une annonce</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Ajoutez votre produit agricole pour le rendre visible aux acheteurs</p>', unsafe_allow_html=True)
st.divider()

if "vendeur_id" not in st.session_state:
    st.warning("Vous devez d’abord créer votre profil vendeur avant de publier une annonce.")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("👤 Créer mon profil vendeur", key="create_profile_annonce", use_container_width=True):
            st.switch_page("pages/01_profil.py")
    with col2:
        if st.button("🔑 Se connecter", key="login_annonce", use_container_width=True):
            st.switch_page("pages/03_connexion.py")
    st.stop()

vendeur_id = st.session_state["vendeur_id"]
vendeur_nom = st.session_state.get("vendeur_nom", "Vendeur")
st.info(f"👤 Vendeur connecté : **{vendeur_nom}**")

with st.form("formulaire_annonce", clear_on_submit=False):
    st.markdown('<div class="section-title">📝 Informations de l’annonce</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        produit = st.text_input("Produit *", placeholder="ex. Oignons, mil, tomates")
        prix = st.number_input("Prix (FCFA) *", min_value=0.0, step=100.0, format="%.2f")
    with col2:
        quantite = st.number_input("Quantité *", min_value=1, step=1)
        unite = st.selectbox("Unité *", ["kg", "sac", "litre", "tonne", "caisse", "botte"])
    description = st.text_area("Description (optionnel)", height=120)
    photos = st.file_uploader("Ajouter de 1 à 3 photos *", type=["jpg", "jpeg", "png"], accept_multiple_files=True)
    bouton_publier = st.form_submit_button("📢 Publier l'annonce", use_container_width=True, type="primary")

if photos:
    st.markdown('<div class="section-title">🖼️ Aperçu des photos</div>', unsafe_allow_html=True)
    cols = st.columns(min(len(photos), 3))
    for i, photo in enumerate(photos[:3]):
        with cols[i]:
            st.image(photo, use_container_width=True)

if bouton_publier:
    erreurs = []
    if not produit.strip(): erreurs.append("Produit obligatoire.")
    if prix <= 0: erreurs.append("Prix > 0.")
    if quantite <= 0: erreurs.append("Quantité > 0.")
    if not photos or len(photos) == 0: erreurs.append("Au moins une photo.")
    elif len(photos) > 3: erreurs.append("Maximum 3 photos.")
    if erreurs:
        for err in erreurs:
            st.error(f"⚠️ {err}")
    else:
        chemins_images = []
        for photo in photos:
            ext = photo.name.split(".")[-1].lower()
            nom_unique = f"{uuid4()}.{ext}"
            chemin = os.path.join(UPLOAD_FOLDER, nom_unique)
            with open(chemin, "wb") as f:
                f.write(photo.getbuffer())
            chemins_images.append(chemin)
        annonce = {
            "id": datetime.now().strftime("%Y%m%d%H%M%S%f"),
            "produit": produit.strip(),
            "prix": prix,
            "quantite": quantite,
            "unite": unite,
            "description": description.strip(),
            "photos": chemins_images,
            "vendeur_id": vendeur_id,
            "created_at": datetime.now().isoformat(),
            "actif": True
        }
        save_annonce(annonce)
        st.markdown(f"""
        <div class="success-box">
            ✅ <strong>Annonce publiée avec succès !</strong><br>
            Votre produit <strong>{produit.strip()}</strong> est maintenant visible.
        </div>
        """, unsafe_allow_html=True)
        st.balloons()
        st.rerun()

st.divider()
st.markdown("""
<div style="text-align: center; color: gray; font-size: 0.9em;">
    AgroSénégal © 2026 — Sprint 1 MVP | Développé avec ❤️ à Dakar
</div>
""", unsafe_allow_html=True)