import streamlit as st
from models import get_model_response


def show_chat():
    """
    Muestra la pantalla de chat y gestiona el flujo de la conversación
    utilizando las respuestas reales de los modelos de IA.
    """
    model1 = st.session_state.model1
    model2 = st.session_state.model2
    topic = st.session_state.topic
    
    # Configuración de colores para cada autor
    author_colors = {
        model1: "#E8F4FD",  # Azul claro
        model2: "#F0F8F0",  # Verde claro
        "Customer": "#FFF8E1",  # Amarillo claro
        "AI Assist": "#F5F0FF"  # Morado claro
    }
    
    # Título y tema
    st.title(f"Conversación: {model1} vs. {model2}")
    st.caption(f"Tema: {topic if topic else 'Libre'}")
    
    # Indicador de turno actual
    current_speaker = st.session_state.get("next_speaker", model1)
    st.markdown(f"**Turno actual: {current_speaker}**")
    st.markdown("---")

    # Contenedor para los botones en la misma línea
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Regresar", type="secondary"):
            st.session_state.screen = "config"
            st.rerun()
    
    with col2:
        if st.button("Detener Conversación"):
            st.session_state.stop_conversation = True
            st.warning("La conversación ha sido detenida por el usuario.")
            st.rerun()

    # Muestra el historial de la conversación existente
    for msg in st.session_state.get("conversation", []):
        author = msg["author"]
        content = msg["content"]
        
        # Determinar el color de fondo según el autor
        bg_color = author_colors.get(author, "#F5F5F5")  # Color por defecto
        
        # Crear un contenedor con estilo para cada mensaje
        with st.container():
            st.markdown(
                f"""
                <div style="
                    background-color: {bg_color};
                    border-radius: 10px;
                    padding: 15px;
                    margin: 10px 0;
                    border-left: 5px solid {get_border_color(bg_color)};
                ">
                    <div style="font-weight: bold; margin-bottom: 5px;">{author}</div>
                    <div>{content}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

    # Lógica de la conversación en tiempo real
    if not st.session_state.get("stop_conversation", False):
        current_speaker = st.session_state.next_speaker
        other_speaker = model2 if current_speaker == model1 else model1

        # Define el contexto (prompt de sistema) para el modelo
        if not st.session_state.conversation:
            # Mensaje de sistema para el primer turno
            prompt_context = f"El tema de esta conversación es: '{topic if topic else 'cualquier cosa que desees'}'. Tu respuesta debe ser solo tu primer mensaje, sin preámbulos."
        else:
            # Mensaje de sistema para continuar la conversación
            prompt_context = f"El tema de esta conversación es:  '{topic if topic else 'un tema libre'}'. El historial de la conversación se proporciona a continuación. Continúa la conversación de forma natural. Tu respuesta debe ser solo tu mensaje, sin preámbulos."

        # Genera y muestra la respuesta del modelo
        with st.spinner(f"Esperando a {current_speaker}..."):
            response = get_model_response(
                model_name=current_speaker,
                prompt_context=prompt_context,
                history=st.session_state.conversation,
                current_speaker=current_speaker
            )
        
        # Añade la nueva respuesta al historial
        st.session_state.conversation.append({"author": current_speaker, "content": response})

        # Determina el siguiente orador
        st.session_state.next_speaker = other_speaker

        # Vuelve a ejecutar para mostrar el nuevo mensaje y continuar el ciclo
        st.rerun()


def get_border_color(bg_color):
    """
    Devuelve un color de borde más oscuro basado en el color de fondo.
    """
    color_mapping = {
        "#E8F4FD": "#1E88E5",  # Azul
        "#F0F8F0": "#43A047",  # Verde
        "#FFF8E1": "#FFB300",  # Amarillo
        "#F5F0FF": "#7E57C2"   # Morado
    }
    return color_mapping.get(bg_color, "#757575")  # Gris por defecto