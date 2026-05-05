import streamlit as st
from langchain_community.document_loaders import PyMuPDFLoader
from llm_engine import SummaryEngine
import tempfile

st.set_page_config(page_title="AI Doc Summarizer", page_icon="📑")

st.title("📑 Assistant de Synthèse Automatique")
st.caption("Générez des rapports structurés à partir de vos PDF longs.")

# Sidebar pour la configuration
with st.sidebar:
    api_key = st.text_input("Groq API Key", type="password")
    st.info("Clé récupérée sur console.groq.com")

uploaded_file = st.file_uploader("Charger un document PDF", type="pdf")

if uploaded_file and api_key:
    # Sauvegarde temporaire du fichier pour LangChain
    with tempfile.NamedTemporaryFile(delete=False) as tf:
        tf.write(uploaded_file.getbuffer())
        file_path = tf.name

    if st.button("Lancer l'analyse"):
        with st.spinner("Le LLM analyse le document..."):
            try:
                # 1. Ingestion
                loader = PyMuPDFLoader(file_path)
                data = loader.load()
                
                # 2. Logique métier
                engine = SummaryEngine(api_key)
                result = engine.generate_summary(data)
                
                # 3. Affichage
                st.markdown("---")
                st.subheader("Analyse Terminée")
                st.markdown(result)
                
                st.download_button("Télécharger le résumé", result, file_name="resume.md")
                
            except Exception as e:
                st.error(f"Une erreur est survenue : {e}")
elif not api_key and uploaded_file:
    st.warning("Veuillez entrer votre clé API dans la barre latérale.")