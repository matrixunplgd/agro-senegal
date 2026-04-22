import streamlit as st
 
# ─── CSS ─────────────────────────────────────────────
st.markdown("""
<style>
.bloc-contact {
    background: #e8f5ee;
    border-radius: 12px;
    padding: 16px 18px;
    margin-top: 12px;
}
.contact-label {
    font-size: 0.72rem;
    font-weight: 600;
    color: #1B5E20;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    margin-bottom: 10px;
}
.numero-ligne {
    font-size: 1.05rem;
    font-weight: 500;
    color: #1a1a18;
    margin-bottom: 8px;
}
.btn-appel {
    display: block;
    background: #2E7D32;
    color: white !important;
    text-decoration: none !important;
    padding: 9px 20px;
    border-radius: 8px;
    font-size: 0.9rem;
    font-weight: 500;
    text-align: center;
    margin-bottom: 10px;
}
.btn-appel:hover { background: #388E3C; }
.horaires {
    border-top: 1px dashed rgba(26,92,56,0.25);
    padding-top: 10px;
    font-size: 0.8rem;
    color: #1B5E20;
    line-height: 1.6;
}
.carte-annonce {
    background-color: #F1F8E9;
    padding: 18px 20px;
    border-radius: 10px;
    border-left: 5px solid #2E7D32;
    margin: 10px 0;
}
.carte-titre {
    font-size: 1.15rem;
    font-weight: 700;
    color: #1a1a18;
    margin-bottom: 2px;
}
.carte-vendeur { font-size: 0.85rem; color: #5a5a56; margin-bottom: 6px; }
.carte-prix { font-size: 1.1rem; color: #c47c2b; font-weight: 600; margin-bottom: 4px; }
.note-spam { font-size: 0.72rem; color: #888; margin-top: 8px; font-style: italic; }
</style>
""", unsafe_allow_html=True)
 
 
# ─── Données vendeurs ─────────────────────────────────────────────────────────
VENDEURS = [
    {
        "id": 1,
        "nom_produit": "Légumes frais du jour",
        "vendeur": "Aminata Diallo",
        "marche": "Marché Sandaga",
        "prix": "500 FCFA / kg",
        "telephone": "+221771234567",
        "telephone_affiche": "+221 77 123 45 67",
        "horaires": "Lun – Sam : 7h00 – 13h00",
        "details_horaires": "Heures de marché uniquement",
        "emoji": "🥬"
    },
    {
        "id": 2,
        "nom_produit": "Tomates & poivrons bio",
        "vendeur": "Fatou Mbaye",
        "marche": "Marché HLM",
        "prix": "800 FCFA / kg",
        "telephone": "+221769876543",
        "telephone_affiche": "+221 76 987 65 43",
        "horaires": "Mar – Dim : 6h30 – 12h30",
        "details_horaires": "Matin uniquement",
        "emoji": "🍅"
    },
    {
        "id": 3,
        "nom_produit": "Mil & maïs en gros",
        "vendeur": "Coopérative Thiès-Nord",
        "marche": "Thiès",
        "prix": "250 FCFA / kg",
        "telephone": "+221785551234",
        "telephone_affiche": "+221 78 555 12 34",
        "horaires": "Lun – Ven : 8h00 – 17h00",
        "details_horaires": "Jours ouvrables",
        "emoji": "🌾"
    },
]
 
 
def masquer_numero(tel: str) -> str:
    """US-07 critère 4 — masque le numéro par défaut contre les robots."""
    parties = tel.split(" ")
    if len(parties) >= 4:
        return " ".join(parties[:2] + ["***", "**"] + [parties[-1]])
    return tel[:7] + " *** " + tel[-2:]
 
 
def afficher_carte(vendeur: dict, reveler: bool = False):
    """US-07 — affiche une carte annonce avec le bloc contact complet."""
 
    # Critère 4 : numéro masqué par défaut, révélé après clic
    numero = vendeur["telephone_affiche"] if reveler else masquer_numero(vendeur["telephone_affiche"])
 
    # Critère 2 : lien tel: pour appel direct sur mobile
    lien_tel = "tel:" + vendeur["telephone"]
    prenom = vendeur["vendeur"].split()[0]
 
    # Critère 1 : numéro affiché — Critère 3 : horaires
    # Les commentaires HTML sont retirés du f-string pour éviter le rendu en texte brut
    html = (
        '<div class="carte-annonce">'
        '<div class="carte-titre">' + vendeur["emoji"] + " " + vendeur["nom_produit"] + "</div>"
        '<div class="carte-vendeur">📍 ' + vendeur["vendeur"] + " — " + vendeur["marche"] + "</div>"
        '<div class="carte-prix">' + vendeur["prix"] + "</div>"
        '<div class="bloc-contact">'
        '<div class="contact-label">📞 Contacter le vendeur</div>'
        '<div class="numero-ligne">📱 ' + numero + "</div>"
        '<a href="' + lien_tel + '" class="btn-appel">📞 Appeler ' + prenom + "</a>"
        '<div class="horaires">'
        "<strong>🕗 Horaires recommandés</strong><br>"
        + vendeur["horaires"] + " · " + vendeur["details_horaires"] +
        "</div>"
        "</div>"
        '<div class="note-spam">🔒 Numéro protégé contre les robots</div>"'
        "</div>"
    )
    st.markdown(html, unsafe_allow_html=True)
 
 
# ─── Interface ────────────────────────────────────────────────────────────────
st.markdown('<p style="font-size:2em;font-weight:bold;color:#1B5E20;">📞 Contact vendeurs</p>',
            unsafe_allow_html=True)
st.markdown("Trouvez et contactez directement les vendeurs agricoles.")
st.divider()
 
# Barre de recherche
recherche = st.text_input(
    "🔍 Rechercher un produit ou un vendeur",
    placeholder="Ex : tomates, Sandaga, Aminata…"
)
 
# Filtrage
vendeurs_filtres = [
    v for v in VENDEURS
    if not recherche or any(
        recherche.lower() in str(v[k]).lower()
        for k in ["nom_produit", "vendeur", "marche"]
    )
]
 
if not vendeurs_filtres:
    st.info("Aucun vendeur trouvé.")
else:
    st.markdown(f"**{len(vendeurs_filtres)} annonce(s) trouvée(s)**")
 
    # 2 colonnes — cohérent avec layout="wide" de app.py
    cols = st.columns(2)
    for i, vendeur in enumerate(vendeurs_filtres):
        cle = f"reveler_{vendeur['id']}"
        if cle not in st.session_state:
            st.session_state[cle] = False
 
        with cols[i % 2]:
            afficher_carte(vendeur, reveler=st.session_state[cle])
 
            # Critère 4 : bouton pour révéler/masquer le numéro
            if not st.session_state[cle]:
                if st.button("👁 Voir le numéro complet",
                             key=f"voir_{vendeur['id']}",
                             use_container_width=True):
                    st.session_state[cle] = True
                    st.rerun()
            else:
                if st.button("🙈 Masquer",
                             key=f"masquer_{vendeur['id']}",
                             use_container_width=True):
                    st.session_state[cle] = False
                    st.rerun()