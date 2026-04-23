import streamlit as st
import hashlib
import time
from data.database import get_vendeur_by_phone

st.set_page_config(
    page_title="Connexion — AgroSénégal",
    page_icon="🔑",
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.markdown("""
    <style>
        .main-title { font-size: 2em; color: #1B5E20; font-weight: bold; text-align: center; }
        .block-container { max-width: 420px; margin: auto; padding-top: 2rem; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-title">🌱 AgroSénégal</p>', unsafe_allow_html=True)
st.subheader("🔑 Connexion vendeur")
st.caption("Entrez votre numéro de téléphone et votre mot de passe.")
st.divider()

telephone = st.text_input("📱 Téléphone", placeholder="Ex : 77 123 45 67", key="login_phone")
mot_de_passe = st.text_input("🔒 Mot de passe", type="password", key="login_password")

if st.button("Se connecter", type="primary", use_container_width=True, key="login_btn"):
    tel_clean = telephone.replace(" ", "").replace("-", "")
    if not tel_clean or not mot_de_passe:
        st.error("Veuillez remplir tous les champs.")
    else:
        vendeur = get_vendeur_by_phone(tel_clean)
        if not vendeur:
            st.error("❌ Numéro introuvable. Veuillez vous inscrire.")
        else:
            # Hachage du mot de passe saisi pour comparaison
            hash_saisi = hashlib.sha256(mot_de_passe.encode()).hexdigest()
            # Le mot de passe stocké peut être en clair ou déjà hashé ? Ici on compare en clair (à améliorer)
            if vendeur.get("mot_de_passe") == mot_de_passe or hash_saisi == vendeur.get("mot_de_passe_hash", ""):
                # Stockage en session
                st.session_state["token"] = "ok"
                st.session_state["vendeur_id"] = vendeur["id"]
                st.session_state["vendeur_nom"] = f"{vendeur['prenom']} {vendeur['nom']}"
                st.session_state["vendeur_email"] = vendeur.get("email", "")
                st.session_state["vendeur_phone"] = vendeur["telephone"]
                st.session_state["nom"] = f"{vendeur['prenom']} {vendeur['nom']}"
                st.session_state["quartier"] = vendeur.get("commune", "Dakar")
                st.success(f"✅ Bienvenue {vendeur['prenom']} !")
                time.sleep(1)
                st.switch_page("pages/03_dashboard.py")
            else:
                st.error("❌ Mot de passe incorrect.")

st.divider()
st.markdown("""
<div style="text-align:center; font-size:0.9em; color:#757575;">
    Pas encore de compte ?
</div>
""", unsafe_allow_html=True)
if st.button("📝 Créer mon profil vendeur", use_container_width=True, key="register_btn"):
    st.switch_page("pages/01_profil.py")
if st.button("← Retour à l'accueil", use_container_width=True, key="back_home_btn"):
    st.switch_page("app.py")