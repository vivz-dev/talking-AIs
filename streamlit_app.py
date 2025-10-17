import streamlit as st
from config_screen import show_config
from chat_screen import show_chat

def main():
    """
    Función principal para ejecutar la aplicación Streamlit.
    Gestiona el enrutamiento entre la pantalla de configuración y la de chat.
    """
    
    # Inicializa el estado de la sesión para la gestión de la pantalla si no existe.
    if "screen" not in st.session_state:
        st.session_state.screen = "config"
        
    # Enrutamiento de pantalla basado en el estado de la sesión.
    if st.session_state.screen == "config":
        show_config()
    elif st.session_state.screen == "chat":
        show_chat()

if __name__ == "__main__":
    main()
