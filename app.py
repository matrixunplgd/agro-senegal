import streamlit as st
import pandas as pd

# Configuration de la page
st.set_page_config(
    page_title="AgroSénégal",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
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
    </style>
""", unsafe_allow_html=True)

# En-tête principal
st.markdown('<p class="main-title">🌱 AgroSénégal</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Plateforme de mise en relation agricole à Dakar</p>', unsafe_allow_html=True)

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

# Navigation rapide
st.subheader("🚀 Accès rapide")

col1, col2 = st.columns(2)

with col1:
    st.markdown("**👤 Profils vendeurs populaires ci-dessous**")

    if st.button("📋 Voir les annonces", use_container_width=True, disabled=True):
        st.info("US-08 bientôt disponible")

with col2:
    if st.button("📢 Publier une annonce", use_container_width=True, disabled=True):
        st.info("US-02 bientôt disponible")

    if st.button("🔑 Se connecter", use_container_width=True):
        st.switch_page("pages/03_connexion.py")

st.divider()

st.subheader("📝 Inscription Vendeur")

if 'sms_code' not in st.session_state:
    st.session_state.sms_code = None
if 'verified_phone' not in st.session_state:
    st.session_state.verified_phone = None

from data.database import init_db, add_profile, get_profiles
init_db()

marches_dakar = [
    "Marché Sandaga",
    "Marché Colobane",
    "Marché Tilène", 
    "Marché Medina",
    "Marché HLM V",
    "Marché Parcelles",
    "Marché Grand Dakar"
]

tab1, tab2 = st.tabs(["📱 Inscription", "👥 Tous les profils"])

with tab1:
    with st.form("inscription_form"):
        nom = st.text_input("Nom complet")
        telephone = st.text_input("Téléphone (+221 XX XXX XXXX)")
        localisation = st.text_input("Localisation")
        marche = st.selectbox("Marché", marches_dakar)
        
        col1, col2 = st.columns(2)
        with col1:
            submitted = st.form_submit_button("S'inscrire")
        with col2:
            send_sms = st.form_submit_button("Envoyer SMS validation")
        
        if send_sms and telephone:
            if not st.session_state.verified_phone:
                import random
                code = random.randint(1000, 9999)
                st.session_state.sms_code = code
                st.success(f"Code SMS envoyé à {telephone} : **{code}** (mock)")
                st.info("Entrez le code pour valider.")
            else:
                st.warning("Téléphone déjà validé !")
        
        code_input = st.number_input("Code SMS reçu", min_value=1000, max_value=9999)
    
    validate_sms = st.button("Valider code")
    if validate_sms and st.session_state.sms_code:
        if code_input == st.session_state.sms_code:
            st.session_state.verified_phone = telephone
            st.success("✅ Téléphone validé !")
            st.session_state.sms_code = None
        else:
            st.error("Code incorrect")
        
        if submitted and st.session_state.verified_phone:
            if add_profile(nom, st.session_state.verified_phone, localisation, marche):
                st.success("✅ Profil créé ! Visible ci-dessus.")
                st.rerun()
            else:
                st.error("Téléphone déjà utilisé.")
        elif submitted:
            st.warning("Validez d'abord le téléphone par SMS.")
    
with tab2:
    profiles = get_profiles()
    if profiles:
        st.dataframe(pd.DataFrame(profiles))
    else:
        st.info("Aucun profil inscrit.")

st.subheader("⭐ Vendeurs populaires")

db_profiles = get_profiles()
seller_choices = [p['name'].lower().replace(' ', '-') for p in db_profiles] + ["moustapha-diop", "fatou-sarr"]
seller_id = st.selectbox("Choisir un vendeur :", seller_choices)

demo_sellers = {p['name'].lower().replace(' ', '-'): p for p in db_profiles}
demo_sellers["moustapha-diop"] = {
    "name": "Moustapha Diop",
    "photo": "https://via.placeholder.com/200x200/2E7D32/FFFFFF?text=M.Diop",
    "location": "Sandaga, Dakar",
    "market": "Marché Sandaga",
    "phone": "+221 77 123 4567",
    "rating": 4.8,
    "annonces": [
        {"produit": "Tomates", "prix": "250", "stock": "150 kg", "date": "15/10"},
        {"produit": "Oignons", "prix": "180", "stock": "80 kg", "date": "14/10"},
        {"produit": "Piments", "prix": "450", "stock": "20 kg", "date": "13/10"}
    ]
}
demo_sellers["fatou-sarr"] = {
    "name": "Fatou Sarr",
    "photo": "https://via.placeholder.com/200x200/388E3C/FFFFFF?text=F.Sarr",
    "location": "Colobane, Dakar",
    "market": "Marché Colobane",
    "phone": "+221 78 987 6543",
    "rating": 4.9,
    "annonces": [
        {"produit": "Mangues", "prix": "350", "stock": "50 kg", "date": "15/10"},
        {"produit": "Bananes", "prix": "120", "stock": "200 kg", "date": "14/10"}
    ]
}

seller = demo_sellers[seller_id]

left_col, right_col = st.columns(2)

with left_col:
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, #1B5E20 0%, #388E3C 100%); padding: 2rem; border-radius: 15px; color: white; text-align: center;'>
        <img src='{seller['photo']}' style='width: 150px; height: 150px; border-radius: 50%; border: 5px solid white;'>
        <h2 style='font-size: 2em;'>{seller['name']}</h2>
        <div style='background: rgba(255,255,255,0.2); padding: 0.5rem 1rem; border-radius: 20px; display: inline-block; margin: 0.5rem;'>📍 {seller['location']}</div>
        <div style='background: rgba(255,255,255,0.2); padding: 0.5rem 1rem; border-radius: 20px; display: inline-block; margin: 0.5rem;'>🏪 {seller['market']}</div>
        <p style='font-size: 1.2em;'>⭐ {seller['rating']}/5</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("📞 Contacter", use_container_width=True):
            st.markdown(f"[Appeler {seller['phone']}](tel:{seller['phone']})")
    with col2:
        st.markdown(f"**Tel:** `{seller['phone']}`")

with right_col:
    st.subheader("📋 Annonces actives")
    if seller['annonces']:
        st.dataframe(
            pd.DataFrame(seller['annonces']),
            use_container_width=True,
            hide_index=True,
            column_config={
                "produit": "Produit",
"prix": "Prix (CFA)",
                "stock": "Stock",
                "date": "Date"
            }
        )
    else:
        st.info("Aucune annonce.")

# Removed duplicate inscription section - using single form above

# Footer
st.markdown("""
<div style="text-align: center; color: gray; font-size: 0.9em;">
    AgroSénégal © 2026 — Sprint 1 MVP | Développé avec ❤️ à Dakar
</div>
""", unsafe_allow_html=True)
