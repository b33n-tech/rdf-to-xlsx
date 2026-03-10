import streamlit as st
import pandas as pd
from bs4 import BeautifulSoup
import io

st.title("🗄️ Piot XML Parser (Méthode robuste)")

uploaded_file = st.file_uploader("Upload ton fichier .rdf", type=['rdf', 'xml'])

if uploaded_file is not None:
    # Lecture du contenu
    content = uploaded_file.getvalue()
    soup = BeautifulSoup(content, 'xml') # On utilise 'xml' comme parser
    
    data = []
    
    # On cherche toutes les balises qui semblent être nos articles
    # Généralement, elles contiennent un dcterms:identifier
    for item in soup.find_all('dcterms:identifier'):
        # On remonte au parent pour avoir accès à tout le bloc de l'article
        parent = item.find_parent()
        
        # Extraction sécurisée (si la balise n'existe pas, on met "" ou "N/A")
        title = parent.find('dcterms:title')
        title = title.text.strip() if title else "Sans titre"
        
        citation = parent.find('dcterms:bibliographicCitation')
        citation = citation.text.strip() if citation else "N/A"
        
        url = item.text.strip()
        
        data.append({
            "Titre": title,
            "Citation": citation,
            "URL": url
        })
    
    df = pd.DataFrame(data)
    
    # Suppression des doublons potentiels (si le fichier contient des variantes)
    df = df.drop_duplicates(subset=['URL'])
    
    st.success(f"Parsing terminé ! {len(df)} articles trouvés.")
    st.dataframe(df)
    
    # Export Excel
    towrite = io.BytesIO()
    df.to_excel(towrite, index=False)
    towrite.seek(0)
    
    st.download_button("📥 Télécharger Excel", data=towrite, file_name="sommaire_piot.xlsx")
