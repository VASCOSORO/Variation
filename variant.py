# app.py

import streamlit as st
import requests

# URL de la API de Node.js expuesta por ngrok
API_URL = "https://<subdominio>.ngrok.io"  # Reemplazá <subdominio> con tu subdominio de ngrok

st.title('Batibot')

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

# Mostrar los mensajes y permitir asignarlos a usuarios
for idx, mensaje in enumerate(mensajes):
    st.subheader(f"Mensaje {idx + 1}")
    st.markdown(f"**De:** {mensaje['numero']}")
    
    if mensaje['esMedia']:
        st.markdown(f"**Archivo multimedia:** [Ver archivo]({API_URL}/{mensaje['rutaMedia']})")
    else:
        st.markdown(f"**Mensaje:** {mensaje['mensaje']}")
    
    # Selector para asignar el mensaje a un usuario
    usuario_asignado = st.selectbox('Asignar a un usuario', usuarios, key=f"usuario_{idx}")
    
    # Campo para escribir una respuesta
    respuesta = st.text_input(f"Escribí una respuesta para {mensaje['numero']}", key=f"respuesta_{idx}")
    
    # Botón para enviar la respuesta
    if st.button("Enviar respuesta", key=f"enviar_{idx}"):
        if respuesta.strip() == "":
            st.warning("El mensaje de respuesta no puede estar vacío.")
        else:
            data = {"numero": mensaje['numero'], "mensaje": respuesta}
            try:
                post_response = requests.post(f"{API_URL}/enviar-mensaje", json=data)
                if post_response.status_code == 200:
                    st.success("Mensaje enviado correctamente")
                else:
                    st.error("Error al enviar el mensaje")
            except Exception as e:
                st.error(f"Error al conectar con la API: {e}")
    
    st.markdown("---")
