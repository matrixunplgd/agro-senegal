import streamlit as st
from data.database import load_annonces, get_vendeur_by_id

# ── Configuration de la page ──────────────────────────────────────────────────
st.set_page_config(
    page_title="AgroSénégal — Consulter les annonces",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Style CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
    <style>
        :root {
            --green-dark:   #1B5E20;
            --green-mid:    #2E7D32;
            --green-light:  #388E3C;
            --green-pale:   #F1F8E9;
            --accent:       #66BB6A;
            --gold:         #F9A825;
            --blue:         #1565C0;
        }

        .main-title {
            font-size: 2.4em;
            color: var(--green-dark);
            font-weight: bold;
            text-align: center;
        }

        .subtitle {
            font-size: 1.15em;
            color: var(--green-light);
            text-align: center;
        }

        .filter-box {
            background-color: #F8FFF5;
            border: 1px solid #C8E6C9;
            border-radius: 12px;
            padding: 16px 18px;
            margin-bottom: 18px;
        }

        .annonce-card {
            background-color: white;
            border: 1px solid #E0E0E0;
            border-left: 5px solid var(--green-mid);
            border-radius: 14px;
            padding: 18px;
            margin: 16px 0;
            box-shadow: 0 2px 10px rgba(0,0,0,0.04);
        }

        .annonce-title {
            color: var(--green-dark);
            font-size: 1.35em;
            font-weight: 700;
            margin-bottom: 8px;
        }

        .prix-box {
            font-size: 1.1em;
            font-weight: bold;
            color: #BF360C;
            margin-bottom: 10px;
        }

        .meta-line {
            color: #2f4f2f;
            font-size: 0.96em;
            margin-bottom: 6px;
        }

        .badge {
            display: inline-block;
            padding: 4px 10px;
            border-radius: 999px;
            font-size: 0.82em;
            font-weight: 600;
            margin-right: 8px;
            margin-bottom: 8px;
        }

        .badge-green {
            background-color: #E8F5E9;
            color: #1B5E20;
            border: 1px solid #A5D6A7;
        }

        .badge-gold {
            background-color: #FFF8E1;
            color: #8D6E63;
            border: 1px solid #FFE082;
        }

        .badge-blue {
            background-color: #E3F2FD;
            color: #1565C0;
            border: 1px solid #90CAF9;
        }

        .empty-box {
            background-color: #FFF8E1;
            border: 1px solid #FFE082;
            border-radius: 10px;
            padding: 18px 24px;
            text-align: center;
            color: #6D4C41;
            font-size: 1.05em;
        }

        .section-title {
            color: var(--green-dark);
            font-weight: 700;
            font-size: 1.1em;
            border-bottom: 2px solid var(--accent);
            padding-bottom: 4px;
            margin-bottom: 12px;
        }
    </style>
""", unsafe_allow_html=True)

# ── En-tête ───────────────────────────────────────────────────────────────────
st.markdown('<p class="main-title">📋 Consulter les annonces</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Découvrez les produits agricoles disponibles sur AgroSénégal, sans créer de compte</p>', unsafe_allow_html=True)

st.divider()

annonces = load_annonces()
annonces_actives = [a for a in annonces if a.get("actif", True)]

# ── Préparer les catégories disponibles ───────────────────────────────────────
categories_set = set()

for annonce in annonces_actives:
    vendeur = get_vendeur_by_id(annonce.get("vendeur_id"))
    if vendeur:
        for cat in vendeur.get("categories", []):
            categories_set.add(cat)

categories_options = ["Toutes"] + sorted(categories_set)

# ── Zone filtres ──────────────────────────────────────────────────────────────
st.markdown('<div class="section-title">🔎 Recherche et filtres</div>', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    recherche = st.text_input("Produit", placeholder="ex. tomate, oignon, mil")

with col2:
    commune_filtre = st.text_input("Commune", placeholder="ex. Pikine, Rufisque")

with col3:
    categorie_filtre = st.selectbox("Catégorie", categories_options)

with col4:
    tri_prix = st.selectbox(
        "Trier par prix",
        ["Plus récents", "Prix croissant", "Prix décroissant"]
    )

# ── Filtrage ──────────────────────────────────────────────────────────────────
resultats = []

for annonce in annonces_actives:
    vendeur = get_vendeur_by_id(annonce.get("vendeur_id"))

    vendeur_commune = vendeur.get("commune", "") if vendeur else ""
    vendeur_categories = vendeur.get("categories", []) if vendeur else []

    match_produit = recherche.lower() in annonce.get("produit", "").lower() if recherche else True
    match_commune = commune_filtre.lower() in vendeur_commune.lower() if commune_filtre else True
    match_categorie = categorie_filtre in vendeur_categories if categorie_filtre != "Toutes" else True

    if match_produit and match_commune and match_categorie:
        resultats.append((annonce, vendeur))

# ── Tri ───────────────────────────────────────────────────────────────────────
if tri_prix == "Prix croissant":
    resultats.sort(key=lambda x: x[0].get("prix", 0))
elif tri_prix == "Prix décroissant":
    resultats.sort(key=lambda x: x[0].get("prix", 0), reverse=True)
else:
    resultats.sort(key=lambda x: x[0].get("created_at", ""), reverse=True)

# ── Affichage ─────────────────────────────────────────────────────────────────
if not resultats:
    st.markdown("""
    <div class="empty-box">
        Aucune annonce ne correspond à votre recherche pour le moment.
    </div>
    """, unsafe_allow_html=True)
else:
    st.write(f"**{len(resultats)} annonce(s) trouvée(s)**")

    for annonce, vendeur in resultats:
        produit = annonce.get("produit", "Produit non défini")
        prix = annonce.get("prix", 0)
        quantite = annonce.get("quantite", 0)
        unite = annonce.get("unite", "")
        description = annonce.get("description", "")
        photos = annonce.get("photos", [])
        created_at = annonce.get("created_at", "")

        vendeur_nom = "Vendeur inconnu"
        vendeur_commune = "Non renseignée"
        vendeur_telephone = "Non renseigné"
        vendeur_categories = []
        vendeur_bio = False
        vendeur_livraison = False

        if vendeur:
            vendeur_nom = f"{vendeur.get('prenom', '')} {vendeur.get('nom', '')}".strip()
            vendeur_commune = vendeur.get("commune", "Non renseignée")
            vendeur_telephone = vendeur.get("telephone", "Non renseigné")
            vendeur_categories = vendeur.get("categories", [])
            vendeur_bio = vendeur.get("bio", False)
            vendeur_livraison = vendeur.get("livraison", False)

        st.markdown(f'<div class="annonce-card">', unsafe_allow_html=True)
        st.markdown(f'<div class="annonce-title">🌾 {produit}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="prix-box">{prix} FCFA</div>', unsafe_allow_html=True)

        badges_html = ""
        if vendeur_bio:
            badges_html += '<span class="badge badge-green">🌱 Bio / Naturel</span>'
        if vendeur_livraison:
            badges_html += '<span class="badge badge-blue">🚚 Livraison</span>'
        if vendeur_categories:
            badges_html += f'<span class="badge badge-gold">📦 {vendeur_categories[0]}</span>'

        if badges_html:
            st.markdown(badges_html, unsafe_allow_html=True)

        col_info, col_images = st.columns([2, 1])

        with col_info:
            st.markdown(f"**Quantité :** {quantite} {unite}")
            st.markdown(f"**Description :** {description if description else 'Aucune description'}")
            st.markdown(f"**Vendeur :** {vendeur_nom}")
            st.markdown(f"**Commune :** {vendeur_commune}")
            st.markdown(f"**Téléphone :** {vendeur_telephone}")
            st.markdown(f"**Publié le :** {created_at[:10] if created_at else 'Non disponible'}")

            if vendeur_categories:
                st.markdown(f"**Catégories du vendeur :** {', '.join(vendeur_categories)}")

            st.link_button(
                "📞 Contacter le vendeur",
                f"tel:{vendeur_telephone}" if vendeur_telephone != "Non renseigné" else "#",
                use_container_width=False
            )

        with col_images:
            if photos:
                for photo in photos[:2]:
                    try:
                        st.image(photo, use_container_width=True)
                    except Exception:
                        st.warning("Image indisponible.")
            else:
                st.info("Pas de photo")

        st.markdown('</div>', unsafe_allow_html=True)

st.divider()

# ── Actions rapides ───────────────────────────────────────────────────────────
col_a, col_b = st.columns(2)

with col_a:
    if st.button("🏠 Retour à l’accueil", use_container_width=True):
        st.switch_page("app.py")

with col_b:
    if st.button("👤 Créer un profil vendeur", use_container_width=True):
        st.switch_page("pages/01_profil.py")

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align: center; color: gray; font-size: 0.9em;">
    AgroSénégal © 2026 — Sprint 1 MVP | Développé avec ❤️ à Dakar
</div>
""", unsafe_allow_html=True)