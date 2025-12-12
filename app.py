import streamlit as st
import pandas as pd

st.set_page_config(page_title="Lion Sourcing", page_icon="🦁", layout="wide")

st.title("🦁 Lion Industrie - Sourcing Intelligent")
st.markdown("Moteur de recherche unifié : Catalogues, Emails et Base Interne.")
st.divider()

# CHARGEMENT
@st.cache_data
def load_data():
    try:
        # Lecture avec séparateur point-virgule
        df = pd.read_csv("data.csv", sep=";")
        return df
    except:
        return None

df = load_data()

if df is None:
    st.error("⚠️ Fichier data.csv introuvable.")
    st.stop()

# --- SIDEBAR (FILTRES) ---
st.sidebar.header("🔍 Affiner la recherche")

# 1. Filtre TYPE DE PRODUIT (Fleurs, Huiles...)
# On enlève les valeurs vides
types = sorted([x for x in df['Type_Produit'].unique() if str(x) != 'nan'])
sel_type = st.sidebar.multiselect("Type de Produit", types, default=types)

# 2. Filtre PAYS (Maintenant propre : Italie, France...)
pays = sorted([x for x in df['Pays'].unique() if str(x) != 'nan'])
sel_pays = st.sidebar.multiselect("Pays d'origine", pays, default=pays)

# 3. Filtre SOURCE (D'où vient l'info ?)
sources = sorted([x for x in df['Source'].unique() if str(x) != 'nan'])
sel_source = st.sidebar.multiselect("Source de l'info", sources, default=sources)

# 4. Recherche Mot-Clé
search = st.sidebar.text_input("Recherche textuelle (ex: Gelato)")

# FILTRAGE
mask = (df['Type_Produit'].isin(sel_type)) & \
       (df['Pays'].isin(sel_pays)) & \
       (df['Source'].isin(sel_source))

if search:
    mask = mask & (df['Produit'].str.contains(search, case=False, na=False))

filtered_df = df[mask]

# --- RÉSULTATS ---
col1, col2 = st.columns([1, 3])
col1.metric("Offres trouvées", len(filtered_df))

if not filtered_df.empty:
    st.dataframe(
        filtered_df,
        column_config={
            "Lien": st.column_config.LinkColumn("Lien Original"),
            "Contact": st.column_config.LinkColumn("Email / Contact"),
            "Prix": st.column_config.TextColumn("Prix indicatif"),
        },
        use_container_width=True,
        hide_index=True
    )
else:
    st.warning("Aucun résultat avec ces filtres.")
