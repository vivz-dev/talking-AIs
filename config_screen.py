import streamlit as st

# Los nombres en esta lista DEBEN coincidir exactamente con las claves
# del diccionario MODEL_DISPATCHER en el archivo models.py.
AVAILABLE_MODELS = ["Gemini 1.5 Flash", "GPT-4o-mini"]

def show_config():
    """
    Muestra la pantalla de configuración para preparar la conversación de la IA.
    """
    st.title("Configuración de la Conversación")

    # Selección de modelos
    col1, col2 = st.columns(2)
    with col1:
        model1 = st.selectbox(
            "Selecciona el Modelo de IA 1",
            AVAILABLE_MODELS,
            key="model1_select"
        )
    with col2:
        # Filtra la lista para el segundo modelo para evitar seleccionar el mismo.
        available_models_for_2 = [m for m in AVAILABLE_MODELS if m != model1]
        
        # Comprueba si hay modelos disponibles para el segundo selector.
        if available_models_for_2:
            model2 = st.selectbox(
                "Selecciona el Modelo de IA 2",
                available_models_for_2,
                key="model2_select"
            )
        else:
            # Si solo hay un modelo en total, no se puede seleccionar un segundo.
            st.warning("Añade más modelos para permitir una conversación.")
            model2 = None

    # El resto de la UI solo se muestra si se pueden seleccionar dos modelos distintos.
    if model1 and model2:
        # Selección de quién comienza la conversación
        starter = st.radio(
            "¿Quién comienza la conversación?",
            (model1, model2),
            key="starter_radio"
        )

        # Selección del tema de conversación
        st.subheader("Tema de la Conversación (Opcional)")
        topic_suggestions = ["Tecnología y futuro", "Filosofía de la conciencia", "El arte en la era digital"]
        
        suggestion_container = st.container()
        cols = suggestion_container.columns(len(topic_suggestions))
        for i, suggestion in enumerate(topic_suggestions):
            if cols[i].button(suggestion, key=f"suggestion_{i}"):
                st.session_state.topic_input = suggestion

        topic = st.text_input(
            "O describe el tema tú mismo:",
            key="topic_input",
            placeholder="Ej: El impacto de la IA en la medicina"
        )

        # Botón para iniciar la conversación
        if st.button("Iniciar Conversación", type="primary"):
            st.session_state.model1 = model1
            st.session_state.model2 = model2
            st.session_state.starter = starter
            st.session_state.topic = topic
            
            st.session_state.conversation = []
            st.session_state.stop_conversation = False
            st.session_state.next_speaker = starter

            st.session_state.screen = "chat"
            st.rerun()
    else:
        st.info("Por favor, selecciona dos modelos de IA diferentes para comenzar.")