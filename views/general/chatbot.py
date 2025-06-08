"""
chatbot.py

Módulo que implementa un chatbot basado en el modelo Gemini de Google para asistir a personas con diabetes tipo 2.
Utiliza Streamlit para la interfaz web interactiva.

El chatbot puede responder preguntas sobre el manejo de la diabetes y sugerencias de alimentos, pero **no sustituye el consejo médico profesional**.
"""

import streamlit as st
import google.generativeai as genai

# Configura la API de Gemini con la clave segura
my_api_key = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=my_api_key)

# Modelo de lenguaje utilizado
model = genai.GenerativeModel("gemini-2.0-flash")

# Configuración de la interfaz de usuario
st.title("🤖 Chatbot para diabetes")
st.subheader("¿Tiene dudas sobre el manejo de la diabetes? ¡No dude en preguntar! También puede pedir sugerencias de alimentos.")
st.write("""Este chatbot utiliza inteligencia artificial para ayudar a los usuarios a obtener información sobre el manejo de la diabetes.
            No reemplaza un médico o un nutricionista.""")

# Inicializa el historial del chat
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Hola, soy tu asistente virtual para temas relacionados con la diabetes. ¿En qué puedo ayudarte hoy?"}]

# Muestra el historial de mensajes
for message in st.session_state["messages"]:
    with st.chat_message(message["role"], avatar="🤖"):
        st.markdown(message["content"], unsafe_allow_html=True)

# Entrada del usuario
prompt = st.chat_input("Escriba su pregunta o solicitud aquí...")

if prompt:
    # Guarda el mensaje del usuario
    st.session_state["messages"].append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="😃"):
        st.markdown(prompt, unsafe_allow_html=True)

    # Inicia el chat con el historial anterior
    chat = model.start_chat(history=[{"role": m["role"], "parts": [m["content"]]} for m in st.session_state["messages"][:-1]])

    # Envia el mensaje al usuario
    response = chat.send_message(prompt)
    response_text = response.text
    
    # Guarda y muestra la respuesta del asistente
    st.session_state["messages"].append({"role": "assistant", "content": response_text})
    with st.chat_message("assistant", avatar="🤖"):
        st.markdown(response_text, unsafe_allow_html=True)