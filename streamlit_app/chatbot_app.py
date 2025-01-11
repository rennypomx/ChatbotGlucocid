import streamlit as st
import google.generativeai as genai

# Configurar la clave API de Gemini
genai.configure(api_key="")  # Reemplaza con tu clave API de Gemini

# Prompt base
prompt_base = """
Eres un chatbot diseñado para responder preguntas de manera amigable y clara sobre la Diabetes. Tu nombre es Glucocid. Responde siempre con educación y solo proporciona información relevante. Si no entiendes algo, pide que te lo expliquen. Recuerda que eres un chatbot y no tienes emociones.
"""

# Función para construir el historial de conversación
def build_conversation_prompt(messages):
    conversation = prompt_base
    for msg in messages:
        role = "Usuario" if msg["role"] == "user" else "Chatbot"
        conversation += f"\n{role}: {msg['content']}"
    conversation += "\nChatbot:"  # Preparar el bot para responder
    return conversation

# Función para obtener la respuesta generada por Gemini
def get_generative_response(conversation_prompt):
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(conversation_prompt)
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"

# Inicialización de Streamlit
st.title("Chatbot Glucocid 🤖")

# Obtener el nombre del usuario desde los parámetros de consulta usando st.query_params
username = st.query_params.get("username")

# Mostrar mensaje de bienvenida con el nombre del usuario
if username:
    st.write(f"¡Bienvenido, **{username}**!")

if st.button("Cerrar sesión"):
    # Limpiar el estado de la sesión en Streamlit
    st.session_state.clear()
    # Redirigir al endpoint de cierre de sesión en Django
    logout_url = "http://localhost:8000/logout/"  # Asegúrate de que esta URL sea correcta
    st.write("Redirigiendo al cierre de sesión...")
    st.markdown(f"<meta http-equiv='refresh' content='0; url={logout_url}'>", unsafe_allow_html=True)
    st.stop()  # Detiene la ejecución del código de Streamlit


# Inicializar el estado de la conversación
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar mensajes anteriores
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Entrada del usuario
if user_input := st.chat_input("Escribe tu mensaje aquí:"):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Generar el prompt con el historial completo
    conversation_prompt = build_conversation_prompt(st.session_state.messages)

    # Contenedor dinámico para "Generando respuesta..."
    with st.chat_message("assistant"):
        response_placeholder = st.empty()  # Crear un contenedor vacío
        response_placeholder.markdown("Generando respuesta...")  # Mostrar mensaje temporal
        
        # Generar la respuesta
        response = get_generative_response(conversation_prompt)
        
        # Reemplazar el mensaje temporal con la respuesta del bot
        response_placeholder.markdown(response)
    
    # Almacenar la respuesta en el estado de la sesión
    st.session_state.messages.append({"role": "assistant", "content": response})
