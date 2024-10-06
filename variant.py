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

# Definir los colores asignados a cada usuario
colores_usuarios = {
    'Marian': '#FFDDC1',
    'Emily': '#C1FFD7',
    'Valen': '#C1E1FF',
    'Sofi': '#FFC1E1'
}

# Función para mostrar la columna de un usuario con color
def mostrar_usuario(usuario):
    st.markdown(f"<div style='background-color:{colores_usuarios[usuario]}; padding: 10px; border-radius: 10px;'>", unsafe_allow_html=True)
    st.subheader(f"Solapa de {usuario}", anchor=f"solapa_{usuario}")
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    
    # Reducir el tamaño de los títulos de las columnas
    with col1:
        st.markdown("### Ingreso Nuevo")
        for mensaje in asignaciones[usuario]:
            st.image(default_image_url, width=50)
            st.markdown(f"**{mensaje['nombre'] if 'nombre' in mensaje else mensaje['numero']}**")
            st.markdown(mensaje['mensaje'] if not mensaje.get('esMedia', False) else "Archivo multimedia recibido")
    
    with col2:
        st.markdown("### En Charla")
    
    with col3:
        st.markdown("### Agregando Productos")
    
    with col4:
        st.markdown("### Cliente Con Pedido Esperando Pago")
    
    with col5:
        st.markdown("### Pedido Enviado")
    
    with col6:
        st.markdown("### SandBox")

    st.markdown("</div>", unsafe_allow_html=True)

# Interfaz de la "pileta" principal
if st.session_state.view == 'pileta':
    st.header("Pileta de Mensajes")

    col_pileta, col_marian, col_emily, col_valen, col_sofi = st.columns([2, 1, 1, 1, 1])

    # Mostrar mensajes en la "Pileta"
    with col_pileta:
        st.subheader("Pileta")
        for idx, mensaje in enumerate(mensajes):
            # Mostrar imagen de perfil desde URL predeterminada
            st.image(default_image_url, width=50)
            
            # Mostrar número o nombre
            if 'nombre' in mensaje:
                st.markdown(f"**{mensaje['nombre']}**")
            else:
                st.markdown(f"**{mensaje['numero']}**")
            
            # Mostrar mensaje (si no es multimedia)
            if not mensaje.get('esMedia', False):
                st.markdown(mensaje['mensaje'])
            
            # Seleccionar a qué usuario asignar el mensaje
            usuario_asignado = st.selectbox('Asignar a:', usuarios, key=f"usuario_{idx}")

            # Botón para mover el mensaje a la columna del usuario seleccionado
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
