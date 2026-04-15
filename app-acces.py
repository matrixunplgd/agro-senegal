import streamlit as st

# Configuration de la page
st.set_page_config(
    page_title="AgroSénégal",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="collapsed"  # ✅ AJOUT : sidebar fermée sur mobile
)

# Style CSS personnalisé
st.markdown("""
    <style>
        .main-title {
            font-size: 3em;
            color: #1B5E20;
            font-weight: bold;
            text-align: center;
        }
        .subtitle {
            font-size: 1.3em;
            color: #388E3C;
            text-align: center;
        }
        .card {
            background-color: #F1F8E9;
            padding: 20px;
            border-radius: 10px;
            border-left: 5px solid #2E7D32;
            margin: 10px 0;
        }

        /* ✅ AJOUT : responsive mobile */
        @media (max-width: 768px) {
            .main-title { font-size: 2em; }
            .block-container { padding: 1rem 0.8rem !important; }
        }
    </style>
""", unsafe_allow_html=True)

# En-tête principal
st.markdown('<p class="main-title">🌱 AgroSénégal</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Plateforme de mise en relation agricole à Dakar</p>', unsafe_allow_html=True)

# ✅ AJOUT : bannière accès libre + bouton S'inscrire visible mais non obligatoire
col_info, col_btn = st.columns([3, 1])
with col_info:
    st.info("📖 **Consultation libre** — Parcourez toutes les annonces sans créer de compte.")
with col_btn:
    if st.button("✨ S'inscrire", use_container_width=True):
        st.switch_page("pages/inscription.py")

st.divider()

# Introduction
st.markdown("""
### Bienvenue sur AgroSénégal !
Connectez vendeurs agricoles et acheteurs sur les marchés de Dakar.
""")

# 3 colonnes de présentation
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="card">
        <h3>🧑‍🌾 Vendeurs</h3>
        <p>Publiez vos annonces, gérez vos stocks et trouvez des acheteurs réguliers.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="card">
        <h3>🛒 Acheteurs</h3>
        <p>Comparez les prix, trouvez des produits frais près de chez vous.</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="card">
        <h3>🏪 Restaurants</h3>
        <p>Trouvez des fournisseurs fiables et optimisez vos approvisionnements.</p>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# ✅ AJOUT : aperçu des annonces Dakar accessible sans connexion
st.subheader("🛒 Dernières annonces — Dakar")
st.caption("Aucun compte requis pour consulter.")

annonces = [
    {"emoji": "🍅", "titre": "Tomates fraîches",   "prix": "500 FCFA/kg",  "lieu": "Pikine"},
    {"emoji": "🧅", "titre": "Oignons de Potou",   "prix": "350 FCFA/kg",  "lieu": "Thiaroye"},
    {"emoji": "🌾", "titre": "Mil local",           "prix": "400 FCFA/kg",  "lieu": "Guédiawaye"},
    {"emoji": "🌶️", "titre": "Piments frais",       "prix": "800 FCFA/kg",  "lieu": "Parcelles"},
]

cols = st.columns(2, gap="small")
for i, a in enumerate(annonces):
    with cols[i % 2]:
        st.markdown(f"""
        <div class="card">
            <b>{a['emoji']} {a['titre']}</b><br>
            💰 {a['prix']} &nbsp;|&nbsp; 📍 {a['lieu']}
        </div>
        """, unsafe_allow_html=True)

st.divider()

# Navigation rapide
st.subheader("🚀 Accès rapide")

col1, col2 = st.columns(2)

with col1:
    if st.button("👤 Créer mon profil vendeur", use_container_width=True):
        st.switch_page("pages/01_profil.py")

    if st.button("📋 Voir les annonces", use_container_width=True):
        st.switch_page("pages/consultation.py")

with col2:
    if st.button("📢 Publier une annonce", use_container_width=True):
        st.switch_page("pages/02_annonce.py")

    if st.button("🔑 Se connecter", use_container_width=True):
        st.switch_page("pages/connexion.py")

st.divider()

# Footer
st.markdown("""
<div style="text-align: center; color: gray; font-size: 0.9em;">
    AgroSénégal © 2026 — Sprint 1 MVP | Développé avec ❤️ à Dakar
</div>
""", unsafe_allow_html=True)
