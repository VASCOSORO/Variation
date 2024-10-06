import streamlit as st
import requests
from PIL import Image
import io

# URL de la API de Node.js expuesta por ngrok
API_URL = "https://<subdominio>.ngrok.io"  # Reemplazá <subdominio> con tu URL de ngrok

st.title('CRM - Batibot')

# Lista de usuarios para asignar los mensajes
usuarios = ['Usuario 1', 'Usuario 2', 'Usuario 3', 'Usuario 4']

# Obtener los mensajes desde la API de Node.js
try:
    response = requests.get(f"{API_URL}/mensajes")
    mensajes = response.json()
except Exception as e:
    st.error(f"No se pudo conectar con la API: {e}")
    mensajes = []

st.header("Mensajes de WhatsApp")

# Organizar los mensajes en columnas como CRM
col1, col2, col3 = st.columns([3, 2, 3])

# Procesar cada mensaje y mostrar en columnas
for idx, mensaje in enumerate(mensajes):
    with col1:
        # Mostrar imagen de perfil si existe (en este caso, se usará una imagen predeterminada)
        st.image("default-profile.png", width=50)  # Imagen predeterminada (podés agregar el archivo en tu directorio)
        
        # Mostrar número o nombre
        if 'nombre' in mensaje:
            st.markdown(f"**{mensaje['nombre']}**")
        st.markdown(f"**{mensaje['numero']}**")
        
        # Mostrar mensaje (si no es multimedia)
        if not mensaje.get('esMedia', False):
            st.markdown(mensaje['mensaje'])

    with col2:
        # Selector para asignar a un usuario
        usuario_asignado = st.selectbox('Asignar a:', usuarios, key=f"usuario_{idx}")

        # Botón para asignar el mensaje al usuario seleccionado
        if st.button(f"Asignar {mensaje['numero']}", key=f"asignar_{idx}"):
            st.success(f"Mensaje asignado a {usuario_asignado}")

    with col3:
        # Mostrar el estado del mensaje
        if not mensaje.get('esMedia', False):
            st.markdown(f"Estado: En proceso")
        else:
            st.markdown(f"Archivo multimedia recibido")
        
        # Simulación de envío de respuesta
        respuesta = st.text_input(f"Responder a {mensaje['numero']}", key=f"respuesta_{idx}")
        if st.button(f"Enviar respuesta {mensaje['numero']}", key=f"enviar_{idx}"):
            data = {"numero": mensaje['numero'], "mensaje": respuesta}
            try:
                post_response = requests.post(f"{API_URL}/enviar-mensaje", json=data)
                if post_response.status_code == 200:
                    st.success(f"Respuesta enviada a {mensaje['numero']}")
                else:
                    st.error("Error al enviar la respuesta")
            except Exception as e:
                st.error(f"Error al conectar con la API: {e}")
    st.markdown("---")
