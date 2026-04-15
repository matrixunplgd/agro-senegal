import streamlit as st
import hashlib
import time

st.set_page_config(
    page_title="Inscription — AgroSénégal",
    page_icon="📝",
    layout="centered"
)

# ── INIT USERS ─────────────────────────────────────────
if "users" not in st.session_state:
    st.session_state["users"] = {}

# ── Style ─────────────────────────────────────────────
st.markdown("""
    <style>
        .main-title { font-size: 2em; color: #1B5E20; font-weight: bold; text-align: center; }
        .block-container { max-width: 500px; margin: auto; padding-top: 2rem; }
    </style>
""", unsafe_allow_html=True)

# ── En-tête ───────────────────────────────────────────
st.markdown('<p class="main-title">🌱 AgroSénégal</p>', unsafe_allow_html=True)
st.subheader("📝 Inscription vendeur")
st.caption("Créez votre compte en quelques secondes.")

st.divider()

# ── Formulaire ────────────────────────────────────────
nom = st.text_input("👤 Nom complet")
telephone = st.text_input("📱 Téléphone", placeholder="Ex : 77 123 45 67")
quartier = st.text_input("📍 Quartier")
mot_de_passe = st.text_input("🔒 Mot de passe", type="password")
confirmation = st.text_input("🔒 Confirmer le mot de passe", type="password")

# ── Bouton inscription ───────────────────────────────
if st.button("Créer un compte", type="primary", use_container_width=True):

    tel_clean = telephone.replace(" ", "").replace("-", "")

    if not nom or not tel_clean or not quartier or not mot_de_passe or not confirmation:
        st.error("❌ Tous les champs sont obligatoires.")

    elif mot_de_passe != confirmation:
        st.error("❌ Les mots de passe ne correspondent pas.")

    elif tel_clean in st.session_state["users"]:
        st.error("❌ Ce numéro existe déjà.")

    else:
        password_hash = hashlib.sha256(mot_de_passe.encode()).hexdigest()

        # ✅ STOCKAGE
        st.session_state["users"][tel_clean] = {
            "nom": nom,
            "quartier": quartier,
            "password_hash": password_hash
        }

        st.success("✅ Compte créé avec succès !")
        time.sleep(1)

        # ✅ redirection correcte
        st.switch_page("pages/03_connexion.py")

st.divider()

# ── Retour ───────────────────────────────────────────
if st.button("← Retour à la connexion", use_container_width=True):
    st.switch_page("pages/03_connexion.py")