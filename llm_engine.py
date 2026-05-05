# --- LES IMPORTS (Tout en haut) ---
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# --- LA CLASSE (Juste après les imports) ---
class SummaryEngine:
    def __init__(self, api_key):
        # Initialisation du modèle avec la clé reçue depuis app.py
        self.llm = ChatGroq(
            temperature=0, 
            model="llama-3.1-8b-instant", 
            api_key="api_key"
        )

    def generate_summary(self, docs):
        # Transformation de la liste de documents en une seule chaîne de texte
        full_text = "\n".join([doc.page_content for doc in docs])
        
        # Sécurité : on limite à 30 000 caractères pour ne pas dépasser les limites
        text_to_analyze = full_text[:30000] 

        # Définition des instructions pour l'IA
        prompt = ChatPromptTemplate.from_messages([
            ("system", "Tu es un assistant expert en synthèse. Réponds toujours en français."),
            ("user", "Fais un résumé structuré, clair et professionnel du texte suivant :\n\n{text}")
        ])

        # Création de la chaîne de traitement (Pipeline)
        chain = prompt | self.llm | StrOutputParser()

        # Exécution et retour du résultat
        return chain.invoke({"text": text_to_analyze})