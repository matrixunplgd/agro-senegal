import streamlit as st
from data.database import load_annonces, get_vendeur_by_id

st.set_page_config(
    page_title="AgroSénégal — Consulter les annonces",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
        .main-title { font-size: 2.4em; color: #1B5E20; font-weight: bold; text-align: center; }
        .subtitle { font-size: 1.15em; color: #388E3C; text-align: center; }
        .annonce-card {
            background-color: white;
            border-left: 5px solid #2E7D32;
            border-radius: 14px;
            padding: 18px;
            margin: 16px 0;
            box-shadow: 0 2px 10px rgba(0,0,0,0.04);
        }
        .annonce-title { color: #1B5E20; font-size: 1.35em; font-weight: 700; }
        .prix-box { font-size: 1.1em; font-weight: bold; color: #BF360C; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-title">📋 Consulter les annonces</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Découvrez les produits agricoles disponibles sur AgroSénégal, sans créer de compte</p>', unsafe_allow_html=True)
st.divider()

annonces = load_annonces()
# Ne montrer que les annonces actives (si le champ existe)
annonces_actives = [a for a in annonces if a.get("actif", True)]

recherche = st.text_input("🔍 Rechercher un produit", placeholder="ex. tomate, oignon")
if recherche:
    annonces_actives = [a for a in annonces_actives if recherche.lower() in a.get("produit", "").lower()]

if not annonces_actives:
    st.info("Aucune annonce disponible pour le moment.")
else:
    st.write(f"**{len(annonces_actives)} annonce(s) trouvée(s)**")
    for annonce in annonces_actives:
        vendeur = get_vendeur_by_id(annonce.get("vendeur_id"))
        vendeur_nom = f"{vendeur.get('prenom', '')} {vendeur.get('nom', '')}".strip() if vendeur else "Vendeur inconnu"
        vendeur_tel = vendeur.get("telephone", "Non renseigné") if vendeur else "Non renseigné"
        vendeur_commune = vendeur.get("commune", "") if vendeur else ""

        st.markdown(f"""
        <div class="annonce-card">
            <div class="annonce-title">🌾 {annonce.get('produit', 'Produit')}</div>
            <div class="prix-box">{annonce.get('prix', 0)} FCFA / {annonce.get('unite', 'kg')}</div>
            <div>📦 Quantité : {annonce.get('quantite', 0)} {annonce.get('unite', 'kg')}</div>
            <div>👤 Vendeur : {vendeur_nom} {(' - ' + vendeur_commune) if vendeur_commune else ''}</div>
            <div>📞 Téléphone : {vendeur_tel}</div>
            <div>📅 Publié le : {annonce.get('created_at', '')[:10] if annonce.get('created_at') else 'Date inconnue'}</div>
            <div>📝 {annonce.get('description', '')}</div>
        </div>
        """, unsafe_allow_html=True)

st.divider()
col_a, col_b = st.columns(2)
with col_a:
    if st.button("🏠 Retour à l'accueil", key="back_home_consult", use_container_width=True):
        st.switch_page("app.py")
with col_b:
    if st.button("👤 Créer un profil vendeur", key="create_profile_consult", use_container_width=True):
        st.switch_page("pages/01_profil.py")