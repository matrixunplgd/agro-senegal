import streamlit as st

st.set_page_config(
    page_title="Inscription — AgroSénégal",
    page_icon="📝",
    layout="centered"
)

st.markdown("""
    <style>
        .main-title { font-size: 2em; color: #1B5E20; font-weight: bold; text-align: center; }
        .block-container { max-width: 500px; margin: auto; padding-top: 2rem; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-title">🌱 AgroSénégal</p>', unsafe_allow_html=True)
st.subheader("📝 Inscription vendeur")

st.info("📝 L'inscription se fait via le formulaire complet de création de profil qui vous guidera étape par étape.")

st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    if st.button("👤 Créer mon profil vendeur", use_container_width=True, key="go_to_profil_inscription"):
        st.switch_page("pages/01_profil.py")

with col2:
    if st.button("← Retour à la connexion", use_container_width=True, key="back_to_login_inscription"):
        st.switch_page("pages/03_connexion.py")

st.markdown("---")
st.markdown("""
<div style="text-align: center; color: gray; font-size: 0.9em;">
    AgroSénégal © 2026 — Sprint 1 MVP | Développé avec ❤️ à Dakar
</div>
""", unsafe_allow_html=True)