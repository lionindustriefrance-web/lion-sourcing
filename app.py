import streamlit as st
import pandas as pd

# CONFIGURATION DE LA PAGE
st.set_page_config(page_title="Lion Sourcing", page_icon="🦁", layout="wide")

# TITRE
st.title("🦁 Lion Industrie - Moteur de Sourcing")
st.markdown("Recherchez parmi les catalogues PDF, les offres par email et la base interne.")
st.divider()

# CHARGEMENT DES DONNÉES
@st.cache_data
def load_data():
    try:
        # On force la lecture en point-virgule
        df = pd.read_csv("data.csv", sep=";")
        return df
    except Exception as e:
        return None

df = load_data()

if df is None:
    st.error("⚠️ Erreur critique : Le fichier 'data.csv' est introuvable ou mal formaté.")
    st.stop()

# BARRE LATÉRALE (FILTRES)
st.sidebar.header("🔍 Filtres")

# 1. Filtre CATEGORIE (PDF vs Offre Mail vs Fleurs...)
cats = sorted(df['Categorie'].astype(str).unique())
selected_cat = st.sidebar.multiselect("Source / Catégorie", cats, default=cats)

# 2. Filtre PAYS
pays_list = sorted(df['Pays'].astype(str).unique())
selected_pays = st.sidebar.multiselect("Pays", pays_list, default=pays_list)

# 3. Recherche textuelle (Pour trouver "Gelato" ou "Amnesia")
search_term = st.sidebar.text_input("Recherche par mot-clé (ex: Amnesia)")

# 4. Filtre PRIX
# On convertit en nombres pour être sûr, les erreurs deviennent 0
df['Prix'] = pd.to_numeric(df['Prix'], errors='coerce').fillna(0)
min_p = int(df['Prix'].min())
max_p = int(df['Prix'].max())
if max_p > 0:
    price_filter = st.sidebar.slider("Prix Max (€)", min_p, max_p, max_p)
else:
    price_filter = 10000

# FILTRAGE DU TABLEAU
mask = (df['Categorie'].isin(selected_cat)) & (df['Pays'].isin(selected_pays)) & (df['Prix'] <= price_filter)

if search_term:
    # Recherche insensible à la casse dans le nom du produit
    mask = mask & (df['Produit'].str.contains(search_term, case=False, na=False))

filtered_df = df[mask]

# AFFICHAGE DES RÉSULTATS
st.metric("Résultats trouvés", len(filtered_df))

if not filtered_df.empty:
    st.dataframe(
        filtered_df,
        column_config={
            "Lien": st.column_config.LinkColumn("Lien / Source"),
            "Prix": st.column_config.NumberColumn("Prix", format="%.2f €"),
            "Date": st.column_config.DateColumn("Date info"),
        },
        hide_index=True,
        use_container_width=True
    )
else:
    st.info("Aucun résultat. Essayez d'élargir les filtres.")
