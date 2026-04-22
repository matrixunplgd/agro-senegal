import streamlit as st
import hashlib
import time

st.set_page_config(
    page_title="Connexion — AgroSénégal",
    page_icon="🔑",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ── INIT USERS ─────────────────────────────────────────
if "users" not in st.session_state:
    st.session_state["users"] = {
        "771234567": {
            "nom": "Mamadou Diallo",
            "quartier": "Pikine",
            "password_hash": hashlib.sha256("passer123".encode()).hexdigest(),
        }
    }

UTILISATEURS = st.session_state["users"]

# ── Si déjà connecté ──────────────────────────────────
if st.session_state.get("token"):
    st.switch_page("dashboard")

# ── Style ─────────────────────────────────────────────
st.markdown("""
    <style>
        .main-title { font-size: 2em; color: #1B5E20; font-weight: bold; text-align: center; }
        .block-container { max-width: 420px; margin: auto; padding-top: 2rem; }
    </style>
""", unsafe_allow_html=True)

# ── En-tête ───────────────────────────────────────────
st.markdown('<p class="main-title">🌱 AgroSénégal</p>', unsafe_allow_html=True)
st.subheader("🔑 Connexion vendeur")
st.caption("Entrez votre numéro de téléphone et votre mot de passe.")

st.divider()

# ── Formulaire ────────────────────────────────────────
telephone = st.text_input("📱 Téléphone", placeholder="Ex : 77 123 45 67")
mot_de_passe = st.text_input("🔒 Mot de passe", type="password")

# ── Connexion ────────────────────────────────────────
if st.button("Se connecter", type="primary", use_container_width=True):

    tel_clean = telephone.replace(" ", "").replace("-", "")

    if not tel_clean or not mot_de_passe:
        st.error("Veuillez remplir tous les champs.")

    elif tel_clean not in UTILISATEURS:
        st.error("❌ Numéro introuvable.")

    else:
        user = UTILISATEURS[tel_clean]
        hash_saisi = hashlib.sha256(mot_de_passe.encode()).hexdigest()

        if hash_saisi != user["password_hash"]:
            st.error("❌ Mot de passe incorrect.")
        else:
            st.session_state["token"] = "ok"
            st.session_state["nom"] = user["nom"]
            st.session_state["quartier"] = user["quartier"]

            st.success(f"✅ Bienvenue {user['nom']} !")
            time.sleep(1)
            st.switch_page("pages/03_dashboard.py")

st.divider()

# ── Inscription ───────────────────────────────────────
st.markdown("""
<div style="text-align:center; font-size:0.9em; color:#757575;">
    Pas encore de compte ?
</div>
""", unsafe_allow_html=True)

if st.button("📝 S'inscrire gratuitement", use_container_width=True):
    st.switch_page("pages/03_inscription.py")

st.markdown("<br>", unsafe_allow_html=True)

# ── Retour accueil ────────────────────────────────────
if st.button("← Retour à l'accueil", use_container_width=True):
    st.switch_page("app-acces.py")  # si existe sinon supprimer