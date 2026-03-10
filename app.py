import streamlit as st
import pandas as pd
from rdflib import Graph, Namespace

def parse_persee_rdf(uploaded_file):
    g = Graph()
    g.parse(uploaded_file, format="xml")
    
    # Définition des namespaces basés sur ton exemple
    DCTERMS = Namespace("http://purl.org/dc/terms/")
    BIBO = Namespace("http://purl.org/ontology/bibo/")
    
    data = []
    
    # On boucle sur tous les documents
    for s, p, o in g.triples((None, None, BIBO.Document)):
        # On ne garde que ceux qui finissent par #Web pour éviter les doublons
        if "#Web" in str(s):
            doc = s
            # On extrait les infos en visant explicitement les propriétés
            title = g.value(doc, DCTERMS.title)
            citation = g.value(doc, DCTERMS.bibliographicCitation)
            url = g.value(doc, DCTERMS.identifier)
            
            data.append({
                "Titre": str(title) if title else "N/A",
                "Citation": str(citation) if citation else "N/A",
                "URL": str(url) if url else str(doc)
            })
    return pd.DataFrame(data)

# Dans ton app Streamlit :
# ... (après l'upload)
df = parse_persee_rdf(uploaded_file)
st.dataframe(df)
