import streamlit as st
import pandas as pd
from rdflib import Graph, Namespace

st.set_page_config(page_title="Convertisseur RDF Piot", layout="centered")

st.title("🗄️ Convertisseur RDF vers Excel")
st.write("Upload ton fichier `.rdf` de Persée pour le transformer en un tableau Excel propre.")

# Namespace utile pour les métadonnées Dublin Core
DC = Namespace("http://purl.org/dc/elements/1.1/")

uploaded_file = st.file_uploader("Choisis ton fichier .rdf", type=['rdf', 'xml'])

if uploaded_file is not None:
    with st.spinner('Parsing du fichier en cours...'):
        # Charger le graphe RDF
        g = Graph()
        g.parse(uploaded_file, format="xml")
        
        data = []
        # Parcourir tous les sujets qui sont des articles (ou ressources)
        for s in g.subjects(None, None):
            # Extraire les métadonnées basiques
            title = str(g.value(s, DC.title)) if g.value(s, DC.title) else "Sans titre"
            creator = str(g.value(s, DC.creator)) if g.value(s, DC.creator) else "Inconnu"
            date = str(g.value(s, DC.date)) if g.value(s, DC.date) else "Date inconnue"
            url = str(s) # L'URL Persée est souvent le sujet lui-même
            
            data.append({
                "Titre": title,
                "Auteur": creator,
                "Année": date,
                "Lien": url
            })
        
        df = pd.DataFrame(data)
        
        # Nettoyage : retirer les entrées vides ou les doublons
        df = df.drop_duplicates()
        
        st.success(f"Conversion terminée ! {len(df)} articles trouvés.")
        st.dataframe(df.head())
        
        # Bouton de téléchargement
        output_file = "sommaire_piot.xlsx"
        df.to_excel(output_file, index=False)
        
        with open(output_file, "rb") as f:
            st.download_button(
                label="📥 Télécharger le fichier Excel",
                data=f,
                file_name="sommaire_piot.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
