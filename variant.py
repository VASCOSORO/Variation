import streamlit as st
import requests

# URL de la API de Node.js expuesta por ngrok
API_URL = "https://839c-186-128-183-44.ngrok-free.app"  # Reemplazá con la URL pública de ngrok

# Lista de usuarios para asignar los mensajes
usuarios = ['Marian', 'Emily', 'Valen', 'Sofi']

# Diccionario para almacenar los mensajes asignados a cada usuario
asignaciones = {usuario: [] for usuario in usuarios}

st.title('CRM - Batibot')

# Obtener los mensajes desde la API de Node.js
try:
    response = requests.get(f"{API_URL}/mensajes")
    mensajes = response.json()
except Exception as e:
    st.error(f"No se pudo conectar con la API: {e}")
    mensajes = []

st.header("Mensajes de WhatsApp")

# Crear las cinco columnas: Pileta, Marian, Emily, Valen, Sofi
col_pileta, col_marian, col_emily, col_valen, col_sofi = st.columns([2, 1, 1, 1, 1])

# URL pública para la imagen predeterminada
default_image_url = "https://via.placeholder.com/50"

# Diccionario temporal para asignar los mensajes a usuarios
asignaciones_temp = {usuario: [] for usuario in usuarios}

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
            asignaciones_temp[usuario_asignado].append(mensaje)
            st.success(f"Mensaje asignado a {usuario_asignado}")

# Mostrar los mensajes asignados a Marian
with col_marian:
    st.subheader("Marian")
    for mensaje in asignaciones_temp['Marian']:
        st.image(default_image_url, width=50)
        st.markdown(f"**{mensaje['nombre'] if 'nombre' in mensaje else mensaje['numero']}**")
        st.markdown(mensaje['mensaje'] if not mensaje.get('esMedia', False) else "Archivo multimedia recibido")

# Mostrar los mensajes asignados a Emily
with col_emily:
    st.subheader("Emily")
    for mensaje in asignaciones_temp['Emily']:
        st.image(default_image_url, width=50)
        st.markdown(f"**{mensaje['nombre'] if 'nombre' in mensaje else mensaje['numero']}**")
        st.markdown(mensaje['mensaje'] if not mensaje.get('esMedia', False) else "Archivo multimedia recibido")

# Mostrar los mensajes asignados a Valen
with col_valen:
    st.subheader("Valen")
    for mensaje in asignaciones_temp['Valen']:
        st.image(default_image_url, width=50)
        st.markdown(f"**{mensaje['nombre'] if 'nombre' in mensaje else mensaje['numero']}**")
        st.markdown(mensaje['mensaje'] if not mensaje.get('esMedia', False) else "Archivo multimedia recibido")

# Mostrar los mensajes asignados a Sofi
with col_sofi:
    st.subheader("Sofi")
    for mensaje in asignaciones_temp['Sofi']:
        st.image(default_image_url, width=50)
        st.markdown(f"**{mensaje['nombre'] if 'nombre' in mensaje else mensaje['numero']}**")
        st.markdown(mensaje['mensaje'] if not mensaje.get('esMedia', False) else "Archivo multimedia recibido")
