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
    
    st.title(f"Conversación: {model1} vs. {model2}")
    st.caption(f"Tema: {topic if topic else 'Libre'}")

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
        with st.chat_message(name=msg["author"]):
            st.write(msg["content"])
            
    # Lógica de la conversación en tiempo real
    if not st.session_state.get("stop_conversation", False):
        current_speaker = st.session_state.next_speaker
        other_speaker = model2 if current_speaker == model1 else model1

        # Define el contexto (prompt de sistema) para el modelo
        if not st.session_state.conversation:
            # Mensaje de sistema para el primer turno
            prompt_context = f"Eres {current_speaker}. Inicia una conversación con {other_speaker}. El tema es: '{topic if topic else 'cualquier cosa que desees'}'. Tu respuesta debe ser solo tu primer mensaje, sin preámbulos."
        else:
            # Mensaje de sistema para continuar la conversación
            prompt_context = f"Eres {current_speaker}. Estás en una conversación con {other_speaker} sobre '{topic if topic else 'un tema libre'}'. El historial de la conversación se proporciona a continuación. Continúa la conversación de forma natural. Tu respuesta debe ser solo tu mensaje, sin preámbulos."

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