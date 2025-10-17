import os
import streamlit as st
from openai import OpenAI
import google.generativeai as genai

# --- Inicialización de Clientes ---

# Intenta inicializar los clientes de las APIs.
# Muestra un error en la app si las claves no están configuradas.

# OpenAI (para DeepSeek y GPT)

try:
    openAI_client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
except Exception:
    st.error("Clave de API de OpenAI no encontrada. Por favor, configúrala.")
    openAI_client = None

# Gemini - VERSIÓN CORREGIDA
try:
    # Primero intenta con st.secrets (recomendado para Streamlit)
    if "GOOGLE_API_KEY" in st.secrets:
        google_api_key = st.secrets["GOOGLE_API_KEY"]
    else:
        # Fallback a variables de entorno
        google_api_key = os.environ.get("GOOGLE_API_KEY")
    
    if google_api_key:
        genai.configure(api_key=google_api_key)
        gemini_model = genai.GenerativeModel('gemini-flash-latest')
    else:
        gemini_model = None
        st.error("Clave GOOGLE_API_KEY no encontrada. Configúrala en .streamlit/secrets.toml o en un archivo .env.")
except Exception as e:
    st.error(f"Ocurrió un error al inicializar Gemini: {e}")
    gemini_model = None

# --- Funciones Específicas del Modelo ---
def get_gemini_answer(prompt_context, history, current_speaker):
    """Llama a la API de Gemini con el historial formateado."""
    if not gemini_model:
        return "El cliente de Gemini no está inicializado. Verifica tu clave de API en .streamlit/secrets.toml."
    
    try:
        formatted_history = []
        for msg in history:
            role = 'model' if msg['author'] == current_speaker else 'user'
            formatted_history.append({'role': role, 'parts': [{'text': msg['content']}]})
            
        full_prompt = [
            {'role': 'user', 'parts': [{'text': prompt_context}]}
        ] + formatted_history
        
        response = gemini_model.generate_content(contents=full_prompt)
        return response.text
        
    except Exception as e:
        return f"Error al llamar a Gemini: {str(e)}"

def get_gpt_answer(prompt_context, history, current_speaker):
    """Llama a la API de OpenAI con el historial formateado."""
    if not openAI_client:
        return "El cliente de OpenAI no está inicializado. Verifica tu clave de API."

    messages = [{"role": "system", "content": prompt_context}]
    for msg in history:
        role = "assistant" if msg['author'] == current_speaker else "user"
        messages.append({"role": role, "content": msg['content']})

    response = openAI_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages
    )
    return response.choices[0].message.content

# --- Despachador Principal ---
MODEL_DISPATCHER = {
    "Gemini 1.5 Flash": get_gemini_answer,
    "GPT-4o-mini": get_gpt_answer,
}

def get_model_response(model_name, prompt_context, history, current_speaker):
    """
    Función principal que selecciona y llama al modelo de IA correcto.
    """
    if model_name in MODEL_DISPATCHER:
        return MODEL_DISPATCHER[model_name](prompt_context, history, current_speaker)
    else:
        return f"Error: Modelo '{model_name}' no encontrado."
