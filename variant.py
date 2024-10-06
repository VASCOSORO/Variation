import streamlit as st
import requests

# URL de la API de Node.js expuesta por ngrok (o tu servidor local)
API_URL = "https://839c-186-128-183-44.ngrok-free.app"  # Cambia esto si usas ngrok

# Lista de usuarios y etapas
usuarios = ['Marian', 'Emily', 'Valen', 'Sofi']
etapas = ['Ingreso Nuevo', 'En Charla', 'Agregando Productos', 'Esperando Pago', 'Pedido Enviado', 'SandBox']

# Diccionario para almacenar los mensajes asignados y sus etapas
asignaciones = {usuario: {'Ingreso Nuevo': [], 'En Charla': [], 'Agregando Productos': [], 'Esperando Pago': [], 'Pedido Enviado': [], 'SandBox': []} for usuario in usuarios}

# Obtener los mensajes desde la API de Node.js
try:
    response = requests.get(f"{API_URL}/mensajes")  # Conectando a la API de Node.js
    mensajes = response.json()  # Parsear la respuesta JSON
    st.session_state.mensajes_pileta = mensajes  # Guardar los mensajes en el estado de Streamlit
except Exception as e:
    st.error(f"No se pudo conectar con la API: {e}")

# Mostrar mensajes en la "Pileta"
st.header("Pileta de Mensajes")

for idx, mensaje in enumerate(st.session_state.mensajes_pileta):
    col1, col2 = st.columns([1, 3])
    with col1:
        # Mostrar la imagen del perfil (si existe)
        imagen_url = mensaje.get('rutaMedia', "https://via.placeholder.com/50")
        st.image(imagen_url, width=50)
        st.markdown(f"**{mensaje['numero']}**")

    with col2:
        st.markdown(f"**{mensaje['mensaje']}**")
        usuario_asignado = st.selectbox('Asignar a:', usuarios, key=f"usuario_{idx}")

    if st.button(f"Asignar {mensaje['numero']}", key=f"asignar_{idx}"):
        asignaciones[usuario_asignado]['Ingreso Nuevo'].append(mensaje)
        # Eliminar mensaje de la pileta
        st.session_state.mensajes_pileta.pop(idx)
        st.success(f"Mensaje asignado a {usuario_asignado}")

