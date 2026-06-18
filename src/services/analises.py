from google import genai
import streamlit as st
from typing import Dict, Any


def get_client():
    """
    Inicializa o cliente usando o novo SDK 'google-genai'.
    nicializa o cliente do novo SDK google-genai.
    O uso de cache_resource é fundamental no Streamlit para evitar
    múltiplas instâncias do cliente."""
    try:
        api_key = st.secrets["GOOGLE_API_KEY"]
        # No novo SDK, inicializamos o Client diretamente com a chave
        return genai.Client(api_key=api_key)
    except Exception as e:
        st.error(f"Erro ao configurar o cliente Google GenAI: {e}")
        st.error(f"Configuração falhou: {e}")
    return None


def analyze_metrics_with_ai(metrics: Dict[str, Any], context: str = "") -> str:
    """
    Envia métricas estatísticas para o Gemini analisar.
    """
    model = get_client()
    if not model:
        return "Erro: Modelo não configurado. Verifique sua API Key nos Secrets."

    # Prompt técnico para evitar alucinações e focar em dados
    prompt = f"""
    Contexto: {context}
    Analise tecnicamente estas métricas de imagem (Modo Escuro):
    {metrics}
    
    Forneça:
    1. Diagnóstico de qualidade (exposição e ruído).
    2. Sugestão de ajuste.
    Seja breve.
    """

    try:
        response = model.models.generate_content(model='gemini-2.0-flash', contents=prompt)
        return response.text
    except Exception as e:
        return f"Erro na análise: {str(e)}"
