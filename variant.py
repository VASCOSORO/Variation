import streamlit as st
import requests

# URL de la API de Node.js expuesta por ngrok
API_URL = "https://839c-186-128-183-44.ngrok-free.app"  # Reemplazá con la URL pública de ngrok

# Lista de usuarios para asignar los mensajes
usuarios = ['Marian', 'Emily', 'Valen', 'Sofi']

# Diccionario para almacenar los mensajes asignados a cada usuario
asignaciones = {usuario: [] for usuario in usuarios}

# Estado inicial de la app
if 'view' not in st.session_state:
    st.session_state.view = 'pileta'

st.title('CRM - Batibot')

# Obtener los mensajes desde la API de Node.js
try:
    response = requests.get(f"{API_URL}/mensajes")
    mensajes = response.json()
except Exception as e:
    st.error(f"No se pudo conectar con la API: {e}")
    mensajes = []

# URL pública para la imagen predeterminada
default_image_url = "https://via.placeholder.com/50"

# Función para mostrar la columna de un usuario con color y más vida
def mostrar_usuario(usuario):
    st.markdown(f"<div style='background-color:{colores_usuarios[usuario]}; padding: 20px; border-radius: 10px;'>", unsafe_allow_html=True)
    st.markdown(f"<h2 style='color:white;'>Solapa de {usuario}</h2>", unsafe_allow_html=True)
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    
    # Reducir el tamaño de los títulos de las columnas
    with col1:
        st.markdown("<h3 style='color:white;'>Ingreso Nuevo</h3>", unsafe_allow_html=True)
        for mensaje in asignaciones[usuario]:
            st.image(default_image_url, width=50)
            st.markdown(f"**{mensaje['nombre'] if 'nombre' in mensaje else mensaje['numero']}**")
            st.markdown(mensaje['mensaje'] if not mensaje.get('esMedia', False) else "Archivo multimedia recibido")
    
    with col2:
        st.markdown("<h3 style='color:white;'>En Charla</h3>", unsafe_allow_html=True)
    
    with col3:
        st.markdown("<h3 style='color:white;'>Agregando Productos</h3>", unsafe_allow_html=True)
    
    with col4:
        st.markdown("<h3 style='color:white;'>Cliente Esperando Pago</h3>", unsafe_allow_html=True)
    
    with col5:
        st.markdown("<h3 style='color:white;'>Pedido Enviado</h3>", unsafe_allow_html=True)
    
    with col6:
        st.markdown("<h3 style='color:white;'>SandBox</h3>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

# Interfaz de la "pileta" principal
if st.session_state.view == 'pileta':
    st.header("Pileta de Mensajes")

    col_pileta, col_marian, col_emily, col_valen, col_sofi = st.columns([2, 1, 1, 1, 1])

    # Mostrar mensajes en la "Pileta"
    with col_pileta:
        st.subheader("Pileta")
        for idx, mensaje in enumerate(mensajes):
            row1, row2 = st.columns([1, 2])  # Ajustar las columnas de imagen y desplegable

            # Columna 1: Imagen y número
            with row1:
                st.image(default_image_url, width=50)
                st.markdown(f"**{mensaje['numero']}**")

            # Columna 2: Mensaje y desplegable de asignación
            with row2:
                st.markdown(f"**{mensaje['mensaje']}**")
                usuario_asignado = st.selectbox('Asignar a:', usuarios, key=f"usuario_{idx}")

            # Botón de asignar, centrado
            if st.button(f"Asignar {mensaje['numero']}", key=f"asignar_{idx}"):
                asignaciones[usuario_asignado].append(mensaje)
                st.success(f"Mensaje asignado a {usuario_asignado}")

    # Botones para cambiar de vista a las solapas de cada usuario
    with col_marian:
        if st.button("Marian"):
            st.session_state.view = 'Marian'

    with col_emily:
        if st.button("Emily"):
            st.session_state.view = 'Emily'

    with col_valen:
        if st.button("Valen"):
            st.session_state.view = 'Valen'

    with col_sofi:
        if st.button("Sofi"):
            st.session_state.view = 'Sofi'

# Mostrar la solapa de Marian
if st.session_state.view == 'Marian':
    mostrar_usuario('Marian')
    if st.button("Volver a la Pileta"):
        st.session_state.view = 'pileta'

# Mostrar la solapa de Emily
if st.session_state.view == 'Emily':
    mostrar_usuario('Emily')
    if st.button("Volver a la Pileta"):
        st.session_state.view = 'pileta'

# Mostrar la solapa de Valen
if st.session_state.view == 'Valen':
    mostrar_usuario('Valen')
    if st.button("Volver a la Pileta"):
        st.session_state.view = 'pileta'

# Mostrar la solapa de Sofi
if st.session_state.view == 'Sofi':
    mostrar_usuario('Sofi')
    if st.button("Volver a la Pileta"):
        st.session_state.view = 'pileta'
