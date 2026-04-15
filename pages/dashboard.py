import streamlit as st

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
        .badge-expiré {
            background: #FFEBEE; color: #C62828;
            border-radius: 12px; padding: 2px 10px;
            font-size: 0.8em; font-weight: 600;
        }
        @media (max-width: 768px) {
            .block-container { padding: 1rem 0.8rem !important; }
        }
    </style>
""", unsafe_allow_html=True)

# ── SÉCURITÉ : vérifier le token ─────────────────────────────────────────────
if not st.session_state.get("token"):
    st.warning("🔒 Accès réservé. Veuillez vous connecter.")
    st.stop()   # bloque tout le reste de la page

# ── DONNÉES VENDEUR depuis la session ─────────────────────────────────────────
nom      = st.session_state.get("nom", "Vendeur")
quartier = st.session_state.get("quartier", "Dakar")
token    = st.session_state.get("token", "")

# ── EN-TÊTE + DÉCONNEXION ─────────────────────────────────────────────────────
col_titre, col_deconnexion = st.columns([4, 1])

with col_titre:
    st.title(f"📊 Tableau de bord")
    st.caption(f"👤 {nom} — 📍 {quartier} &nbsp;|&nbsp; 🔐 Token : `{token[:16]}...`")

with col_deconnexion:
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🚪 Se déconnecter", use_container_width=True):
        # Effacer toute la session
        for key in ["token", "telephone", "nom", "quartier"]:
            st.session_state.pop(key, None)
        st.success("Déconnexion réussie.")
        st.switch_page("app-test.py")

st.divider()

# ── STATISTIQUES ──────────────────────────────────────────────────────────────
st.subheader("📈 Résumé")

c1, c2, c3, c4 = st.columns(4)
stats = [
    ("3",   "Annonces actives",   c1),
    ("12",  "Vues aujourd'hui",   c2),
    ("5",   "Contacts reçus",     c3),
    ("1",   "Annonce expirée",    c4),
]
for val, label, col in stats:
    with col:
        st.markdown(f"""
        <div class="stat-box">
            <div class="stat-number">{val}</div>
            <div class="stat-label">{label}</div>
        </div>
        """, unsafe_allow_html=True)

st.divider()

# ── MES ANNONCES (données de démo, à remplacer par votre BDD) ─────────────────
st.subheader("📋 Mes annonces")

annonces_vendeur = [
    {"emoji": "🍅", "titre": "Tomates fraîches",  "prix": "500 FCFA/kg",  "stock": "200 kg",  "statut": "actif",   "vues": 8,  "contacts": 2},
    {"emoji": "🧅", "titre": "Oignons de Potou",  "prix": "350 FCFA/kg",  "stock": "500 kg",  "statut": "actif",   "vues": 3,  "contacts": 3},
    {"emoji": "🌿", "titre": "Manioc bio",         "prix": "250 FCFA/kg",  "stock": "0 kg",    "statut": "expiré",  "vues": 1,  "contacts": 0},
]

for a in annonces_vendeur:
    badge = f'<span class="badge-actif">✅ Actif</span>' if a["statut"] == "actif" \
            else f'<span class="badge-expiré">⛔ Expiré</span>'

    col_info, col_actions = st.columns([3, 1])

    with col_info:
        st.markdown(f"""
        <div class="card">
            <b>{a['emoji']} {a['titre']}</b> &nbsp; {badge}<br>
            💰 {a['prix']} &nbsp;|&nbsp; 📦 {a['stock']}<br>
            <span style="font-size:0.85em; color:#757575;">
                👁️ {a['vues']} vues &nbsp;|&nbsp; 📞 {a['contacts']} contacts
            </span>
        </div>
        """, unsafe_allow_html=True)

    with col_actions:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.button("✏️ Modifier",   key=f"edit_{a['titre']}",   use_container_width=True)
        st.button("🗑️ Supprimer",  key=f"del_{a['titre']}",    use_container_width=True)

st.divider()

# ── ACTIONS RAPIDES ───────────────────────────────────────────────────────────
st.subheader("🚀 Actions rapides")

col1, col2 = st.columns(2)
with col1:
    if st.button("📢 Publier une nouvelle annonce", use_container_width=True):
        st.switch_page("pages/annonce.py")
with col2:
    if st.button("📋 Voir toutes les annonces", use_container_width=True):
        st.switch_page("pages/consultation.py")
