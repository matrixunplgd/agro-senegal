import streamlit as st
from data.database import get_annonces_by_vendeur, delete_annonce, update_annonce

st.set_page_config(
    page_title="Tableau de bord — AgroSénégal",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
    <style>
        .card {
            background-color: #F1F8E9;
            padding: 18px;
            border-radius: 10px;
            border-left: 5px solid #2E7D32;
            margin: 10px 0;
        }
        .stat-box {
            background: white;
            border: 1px solid #C8E6C9;
            border-radius: 12px;
            padding: 20px;
            text-align: center;
            box-shadow: 0 2px 6px rgba(0,0,0,0.06);
        }
        .stat-number { font-size: 2em; font-weight: bold; color: #2E7D32; }
        .stat-label  { font-size: 0.9em; color: #757575; }
        .badge-actif {
            background: #E8F5E9; color: #2E7D32;
            border-radius: 12px; padding: 2px 10px;
            font-size: 0.8em; font-weight: 600;
        }
        .badge-expire {
            background: #FFEBEE; color: #C62828;
            border-radius: 12px; padding: 2px 10px;
            font-size: 0.8em; font-weight: 600;
        }
    </style>
""", unsafe_allow_html=True)

# Vérification de la connexion
if not st.session_state.get("token"):
    st.warning("🔒 Accès réservé. Veuillez vous connecter.")
    if st.button("🔑 Se connecter", key="login_dashboard_redirect", use_container_width=True):
        st.switch_page("pages/03_connexion.py")
    st.stop()

nom = st.session_state.get("nom", st.session_state.get("vendeur_nom", "Vendeur"))
quartier = st.session_state.get("quartier", "Dakar")

col_titre, col_deconnexion = st.columns([4, 1])
with col_titre:
    st.title("📊 Tableau de bord")
    st.caption(f"👤 {nom} — 📍 {quartier}")
with col_deconnexion:
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🚪 Se déconnecter", key="logout_btn", use_container_width=True):
        for key in ["token", "telephone", "nom", "quartier", "vendeur_id", "vendeur_nom", "vendeur_email", "vendeur_phone", "prenom"]:
            st.session_state.pop(key, None)
        st.success("Déconnexion réussie.")
        st.switch_page("app.py")

st.divider()

# Statistiques (simples)
st.subheader("📈 Résumé")
c1, c2, c3, c4 = st.columns(4)
stats = [("0", "Annonces actives", c1), ("0", "Vues aujourd'hui", c2), ("0", "Contacts reçus", c3), ("0", "Annonce expirée", c4)]
for val, label, col in stats:
    with col:
        st.markdown(f"""
        <div class="stat-box">
            <div class="stat-number">{val}</div>
            <div class="stat-label">{label}</div>
        </div>
        """, unsafe_allow_html=True)

st.divider()
st.subheader("📋 Mes annonces")

vendeur_id = st.session_state.get("vendeur_id")
annonces_vendeur = get_annonces_by_vendeur(vendeur_id) if vendeur_id else []

if not annonces_vendeur:
    st.info("Vous n'avez encore publié aucune annonce.")
else:
    for i, a in enumerate(annonces_vendeur):
        badge = '<span class="badge-actif">✅ Actif</span>' if a.get("actif", True) else '<span class="badge-expire">⛔ Expiré</span>'
        col_info, col_actions = st.columns([3, 1])
        with col_info:
            st.markdown(f"""
            <div class="card">
                <b>🌾 {a.get('produit', 'Sans nom')}</b> &nbsp; {badge}<br>
                💰 {a.get('prix', 0)} FCFA/{a.get('unite', 'kg')} &nbsp;|&nbsp; 📦 {a.get('quantite', 0)} {a.get('unite', 'kg')}<br>
                <span style="font-size:0.85em; color:#757575;">
                    📅 {a.get('created_at', '')[:10]} &nbsp;|&nbsp; 👁️ 0 vues
                </span>
            </div>
            """, unsafe_allow_html=True)
        with col_actions:
            st.markdown("<br><br>", unsafe_allow_html=True)
            if st.button("✏️ Modifier", key=f"edit_btn_{a['id']}", use_container_width=True):
                st.session_state[f"edit_mode_{a['id']}"] = not st.session_state.get(f"edit_mode_{a['id']}", False)
            if st.button("🗑️ Supprimer", key=f"del_btn_{a['id']}", use_container_width=True):
                if delete_annonce(a['id']):
                    st.success("Annonce supprimée !")
                    st.rerun()
                else:
                    st.error("Erreur lors de la suppression.")

        # Formulaire d'édition
        if st.session_state.get(f"edit_mode_{a['id']}", False):
            with st.expander(f"Modifier {a['produit']}", expanded=True):
                with st.form(key=f"edit_form_{a['id']}"):
                    new_produit = st.text_input("Produit", value=a.get('produit', ''))
                    new_prix = st.number_input("Prix (FCFA)", value=float(a.get('prix', 0)), step=100.0)
                    new_quantite = st.number_input("Quantité", value=int(a.get('quantite', 1)), step=1)
                    new_unite = st.selectbox("Unité", ["kg", "sac", "litre", "tonne", "caisse", "botte"], 
                                             index=["kg", "sac", "litre", "tonne", "caisse", "botte"].index(a.get('unite', 'kg')))
                    new_description = st.text_area("Description", value=a.get('description', ''))
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        submit_edit = st.form_submit_button("💾 Enregistrer")
                    with col2:
                        cancel_edit = st.form_submit_button("Annuler")
                    
                    if submit_edit:
                        updated_data = {
                            "produit": new_produit,
                            "prix": new_prix,
                            "quantite": new_quantite,
                            "unite": new_unite,
                            "description": new_description
                        }
                        if update_annonce(a['id'], updated_data):
                            st.success("Annonce mise à jour !")
                            st.session_state[f"edit_mode_{a['id']}"] = False
                            st.rerun()
                        else:
                            st.error("Erreur de mise à jour.")
                    if cancel_edit:
                        st.session_state[f"edit_mode_{a['id']}"] = False
                        st.rerun()

st.divider()
st.subheader("🚀 Actions rapides")
col1, col2 = st.columns(2)
with col1:
    if st.button("📢 Publier une nouvelle annonce", key="publish_new_btn", use_container_width=True):
        st.switch_page("pages/02_annonce.py")
with col2:
    if st.button("📋 Voir toutes les annonces", key="view_all_btn", use_container_width=True):
        st.switch_page("pages/08_consultation.py")

st.markdown("""
<div style="text-align: center; color: gray; font-size: 0.9em; margin-top: 2rem;">
    AgroSénégal © 2026 — Sprint 1 MVP | Développé avec ❤️ à Dakar
</div>
""", unsafe_allow_html=True)