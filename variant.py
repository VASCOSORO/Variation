import streamlit as st
import requests

# URL de la API de Node.js expuesta por ngrok o localhost
API_URL = "https://tu-ngrok-url.ngrok-free.app"  # Cambia esto por la URL de ngrok o tu servidor local

# Lista de usuarios y etapas
usuarios = ['Marian', 'Emily', 'Valen', 'Sofi']
etapas = ['Ingreso Nuevo', 'En Charla', 'Agregando Productos', 'Esperando Pago', 'Pedido Enviado', 'SandBox']

# Diccionario para almacenar los mensajes asignados y sus etapas
asignaciones = {usuario: {'Ingreso Nuevo': [], 'En Charla': [], 'Agregando Productos': [], 'Esperando Pago': [], 'Pedido Enviado': [], 'SandBox': []} for usuario in usuarios}

# Estado inicial de la app
if 'view' not in st.session_state:
    st.session_state.view = 'pileta'

if 'solapa_seleccionada' not in st.session_state:
    st.session_state.solapa_seleccionada = None

# Obtener los mensajes desde la API de Node.js
try:
    response = requests.get(f"{API_URL}/mensajes")
    mensajes = response.json()
    st.session_state.mensajes_pileta = mensajes  # Guardar los mensajes en el estado de Streamlit
except Exception as e:
    st.error(f"No se pudo conectar con la API: {e}")

# Función para mostrar los mensajes asignados a un usuario en su etapa
def mostrar_usuario(usuario):
    st.markdown(f"<h2 style='color:#FF5733;'>Solapa de {usuario}</h2>", unsafe_allow_html=True)
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    
    # Mostrar mensajes por etapa
    for idx, (col, etapa) in enumerate(zip([col1, col2, col3, col4, col5, col6], etapas)):
        with col:
            st.markdown(f"<h3>{etapa}</h3>", unsafe_allow_html=True)
            for mensaje in asignaciones[usuario][etapa]:
                if st.button(f"Ver chat {mensaje['numero']}", key=f"chat_{usuario}_{etapa}_{idx}"):
                    st.session_state.view = 'chat'
                    st.session_state.mensaje_chat = mensaje
                    st.session_state.usuario_chat = usuario
                    st.session_state.etapa_chat = etapa

# Función para la vista de chat
def mostrar_chat():
    mensaje = st.session_state.mensaje_chat
    usuario = st.session_state.usuario_chat
    etapa = st.session_state.etapa_chat

    st.subheader(f"Chat con {mensaje['nombre'] if 'nombre' in mensaje else mensaje['numero']} ({etapa})")
    st.text_area("Chat", value=f"Mensajes enviados y recibidos con {mensaje['numero']}", height=300)

    # Cambiar etapa del cliente
    nueva_etapa = st.selectbox("Cambiar etapa a:", etapas, index=etapas.index(etapa))
    if nueva_etapa != etapa:
        asignaciones[usuario][etapa].remove(mensaje)
        asignaciones[usuario][nueva_etapa].append(mensaje)
        st.session_state.etapa_chat = nueva_etapa
        st.success(f"Etapa cambiada a {nueva_etapa}")

    if st.button("Volver a la Solapa"):
        st.session_state.view = 'pileta'

# Interfaz de la "pileta" principal
if st.session_state.view == 'pileta':
    st.header("Pileta de Mensajes")

    col_pileta, col_marian, col_emily, col_valen, col_sofi = st.columns([2, 1, 1, 1, 1])

    # Mostrar mensajes en la "Pileta"
    with col_pileta:
        st.subheader("Pileta")
        for idx, mensaje in enumerate(st.session_state.mensajes_pileta):
            row1, row2 = st.columns([1, 3])

            with row1:
                st.image(mensaje.get('rutaMedia', "https://via.placeholder.com/50"), width=50)
                st.markdown(f"**{mensaje['numero']}**")

            with row2:
                st.markdown(f"**{mensaje['mensaje']}**")
                usuario_asignado = st.selectbox('Asignar a:', usuarios, key=f"usuario_{idx}")

            if st.button(f"Asignar {mensaje['numero']}", key=f"asignar_{idx}"):
                asignaciones[usuario_asignado]['Ingreso Nuevo'].append(mensaje)
                st.session_state.mensajes_pileta.pop(idx)  # Eliminar mensaje de la pileta
                st.success(f"Mensaje asignado a {usuario_asignado}")

    # Botones para seleccionar la solapa de cada asesora
    with col_marian:
        if st.button("Marian"):
            st.session_state.solapa_seleccionada = 'Marian'

    with col_emily:
        if st.button("Emily"):
            st.session_state.solapa_seleccionada = 'Emily'

    with col_valen:
        if st.button("Valen"):
            st.session_state.solapa_seleccionada = 'Valen'

    with col_sofi:
        if st.button("Sofi"):
            st.session_state.solapa_seleccionada = 'Sofi'

# Mostrar la solapa seleccionada
if st.session_state.solapa_seleccionada:
    mostrar_usuario(st.session_state.solapa_seleccionada)

# Mostrar el chat
if st.session_state.view == 'chat':
    mostrar_chat()
