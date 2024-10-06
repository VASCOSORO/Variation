import streamlit as st
import requests

st.title('CRM - Gestión de Mensajes de WhatsApp')

# Lista de usuarios para asignar los mensajes
usuarios = ['Usuario 1', 'Usuario 2', 'Usuario 3', 'Usuario 4']

# Obtener los mensajes desde la API
response = requests.get("http://localhost:3000/mensajes")
mensajes = response.json()

# Mostrar los mensajes y permitir la asignación a usuarios
for mensaje in mensajes:
    st.write(f"**De:** {mensaje['numero']}")
    st.write(f"**Mensaje:** {mensaje['mensaje']}")
    
    if mensaje['esMedia']:
        st.write(f"**Archivo multimedia:** {mensaje['rutaMedia']}")
    
    # Selector para asignar el mensaje a un usuario
    usuario_asignado = st.selectbox('Asignar a un usuario', usuarios, key=f"usuario_{mensaje['numero']}")
    
    if st.button(f"Responder a {mensaje['numero']}", key=f"responder_{mensaje['numero']}"):
        respuesta = st.text_input(f"Escribí una respuesta para {mensaje['numero']}")
        if st.button("Enviar"):
            data = {"numero": mensaje['numero'], "mensaje": respuesta}
            response = requests.post("http://localhost:3000/enviar-mensaje", json=data)
            if response.status_code == 200:
                st.success("Mensaje enviado correctamente")
            else:
                st.error("Error al enviar el mensaje")

st.sidebar.title("Asignación de Mensajes")
st.sidebar.write("Asignar mensajes a diferentes usuarios para responder en simultáneo.")
