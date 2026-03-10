import streamlit as st
import pandas as pd
from rdflib import Graph, Namespace
import io

# Définition des Namespaces utilisés par Persée
DCTERMS = Namespace("http://purl.org/dc/terms/")
BIBO = Namespace("http://purl.org/ontology/bibo/")
RDF = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")

def parse_persee_rdf(uploaded_file):
    # Important : Streamlit renvoie un objet "UploadedFile"
    # Il faut le transformer en un flux de bytes lisible
    g = Graph()
    bytes_data = uploaded_file.getvalue()
    g.parse(data=bytes_data, format="xml")
    
    data = []
    
    # On cherche tous les sujets qui sont des bibo:Document
    # bibo:Document est une classe dans le graphe
    for s in g.subjects(RDF.type, BIBO.Document):
        # On ne veut que les versions "Web" pour éviter les doublons Print
        if "#Web" in str(s):
            # Extraction des propriétés
            title = g.value(s, DCTERMS.title)
            citation = g.value(s, DCTERMS.bibliographicCitation)
            identifier = g.value(s, DCTERMS.identifier)
            
            data.append({
                "Titre": str(title) if title else "N/A",
                "Citation": str(citation) if citation else "N/A",
                "URL": str(identifier) if identifier else str(s)
            })
            
    return pd.DataFrame(data)

st.title("🗄️ RDF to Excel : Piot Parser")

uploaded_file = st.file_uploader("Upload ton fichier .rdf", type=['rdf', 'xml'])

if uploaded_file is not None:
    try:
        df = parse_persee_rdf(uploaded_file)
        
        if not df.empty:
            st.success(f"Fichier parsé avec succès ! {len(df)} articles trouvés.")
            st.dataframe(df)
            
            # Export Excel
            towrite = io.BytesIO()
            df.to_excel(towrite, index=False, engine='openpyxl')
            towrite.seek(0)
            
            st.download_button(
                label="📥 Télécharger le résultat en Excel",
                data=towrite,
                file_name="sommaire_piot.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        else:
            st.warning("Aucune donnée trouvée. Vérifie bien que le fichier contient des 'bibo:Document'.")
            
    except Exception as e:
        st.error(f"Une erreur est survenue pendant le parsing : {e}")
