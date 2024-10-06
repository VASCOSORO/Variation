import streamlit as st
import requests
import json

# URL de la API de Node.js expuesta por ngrok
API_URL = "https://839c-186-128-183-44.ngrok-free.app"  # Reemplazá con tu URL de ngrok

# Lista de usuarios y etapas
usuarios = ['Marian', 'Emily', 'Valen', 'Sofi']
etapas = ['Ingreso Nuevo', 'En Charla', 'Agregando Productos', 'Esperando Pago', 'Pedido Enviado', 'SandBox']

# Diccionario para almacenar las asignaciones de mensajes
# Inicializar en sesión
if 'asignaciones' not in st.session_state:
    st.session_state.asignaciones = {usuario: {etapa: [] for etapa in etapas} for usuario in usuarios}

# Estado para seleccionar la solapa
if 'solapa_seleccionada' not in st.session_state:
    st.session_state.solapa_seleccionada = None

st.title("CRM - Batibot")

# Función para asignar un mensaje a una asesora
def asignar_mensaje(id_mensaje, usuario):
    url = f"{API_URL}/asignar"
    data = {
        "id": id_mensaje,
        "usuario": usuario
    }
    try:
        response = requests.post(url, json=data)
        response.raise_for_status()
        result = response.json()
        if result['success']:
            st.success(f"Mensaje asignado a {usuario}")
    except requests.exceptions.RequestException as e:
        st.error(f"Error al asignar el mensaje: {e}")

# Función para mostrar la solapa de una asesora
def mostrar_solapa(usuario):
    st.markdown(f"### Solapa de {usuario}")
    for etapa in etapas:
        st.markdown(f"#### {etapa}")
        mensajes = st.session_state.asignaciones[usuario][etapa]
        for mensaje in mensajes:
            col1, col2 = st.columns([3, 1])
            with col1:
                nombre = mensaje.get('nombre', 'Desconocido')
                numero = mensaje.get('numero', 'Sin número')
                st.write(f"**{nombre} ({numero})**")
                st.write(f"Mensaje: {mensaje.get('mensaje', '')}")
            with col2:
                if st.button("Ver Chat", key=f"chat_{mensaje['id']}"):
                    st.session_state.solapa_seleccionada = f"chat_{mensaje['id']}"

    # Botón para volver a la pileta
    if st.button("Volver a la Pileta"):
        st.session_state.solapa_seleccionada = None

# Función para mostrar el chat de un mensaje
def mostrar_chat(mensaje):
    st.markdown(f"### Chat con {mensaje.get('nombre', 'Desconocido')} ({mensaje.get('numero', 'Sin número')})")
    
    # Simulación de chat
    st.text_area("Conversación", value="Aquí aparecerán los mensajes enviados y recibidos.", height=300)
    
    st.text_input("Escribe un mensaje")
    st.file_uploader("Adjuntar archivo", type=['png', 'jpg', 'pdf'])
    
    if st.button("Enviar"):
        st.success("Mensaje enviado")
    
    # Cambio de etapa
    nueva_etapa = st.selectbox("Cambiar etapa a:", etapas, index=etapas.index(mensaje['estado']) if mensaje['estado'] in etapas else 0)
    if nueva_etapa != mensaje['estado']:
        st.write(f"Etapa cambiada a {nueva_etapa}")
        # Aquí deberías implementar la lógica para actualizar la etapa en el backend y en el frontend
    
    # Reasignar a otro usuario
    nuevo_usuario = st.selectbox("Reasignar a:", usuarios, index=usuarios.index(mensaje.get('usuario', 0)) if 'usuario' in mensaje else 0)
    if nuevo_usuario != mensaje.get('usuario', ''):
        asignar_mensaje(mensaje['id'], nuevo_usuario)

    # Botón para volver a la solapa
    if st.button("Volver a la Solapa"):
        st.session_state.solapa_seleccionada = None

# Obtener los mensajes desde la API de Node.js
def obtener_mensajes():
    url = f"{API_URL}/mensajes"
    try:
        response = requests.get(url)
        response.raise_for_status()
        mensajes = response.json()
        return mensajes
    except requests.exceptions.RequestException as e:
        st.error(f"No se pudo conectar con la API: {e}")
        return []

# Actualizar las asignaciones en sesión
def actualizar_asignaciones(mensajes):
    # Limpiar asignaciones actuales
    st.session_state.asignaciones = {usuario: {etapa: [] for etapa in etapas} for usuario in usuarios}
    for mensaje in mensajes:
        estado = mensaje.get('estado', 'Pileta')
        if estado.startswith('Asignado a '):
            usuario = estado.split('Asignado a ')[1]
            if usuario in usuarios:
                st.session_state.asignaciones[usuario]['Ingreso Nuevo'].append(mensaje)

# Obtener y actualizar los mensajes
mensajes = obtener_mensajes()
actualizar_asignaciones(mensajes)

# Mostrar la pileta o la solapa seleccionada
if st.session_state.solapa_seleccionada and st.session_state.solapa_seleccionada.startswith("chat_"):
    # Obtener el ID del mensaje
    id_mensaje = st.session_state.solapa_seleccionada.split("_")[1]
    mensaje = next((m for m in mensajes if m['id'] == id_mensaje), None)
    if mensaje:
        mostrar_chat(mensaje)
    else:
        st.error("Mensaje no encontrado")
else:
    # Mostrar la pileta y las solapas
    st.header("Pileta de Mensajes")
    mensajes_pileta = [m for m in mensajes if m.get('estado') == 'Pileta']
    if mensajes_pileta:
        for mensaje in mensajes_pileta:
            col1, col2, col3 = st.columns([2, 3, 1])
            with col1:
                # Mostrar imagen de perfil si existe
                imagen = mensaje.get('imagen', '')
                if imagen:
                    st.image(imagen, width=50)
                else:
                    st.image("https://via.placeholder.com/50", width=50)
            with col2:
                nombre = mensaje.get('nombre', 'Desconocido')
                numero = mensaje.get('numero', 'Sin número')
                st.write(f"**{nombre} ({numero})**")
                st.write(f"Mensaje: {mensaje.get('mensaje', '')}")
            with col3:
                usuario_asignado = st.selectbox('Asignar a:', usuarios, key=f"select_{mensaje['id']}")
                if st.button("Asignar", key=f"asignar_{mensaje['id']}"):
                    asignar_mensaje(mensaje['id'], usuario_asignado)
    else:
        st.info("No hay mensajes en la pileta.")

    st.header("Asignaciones")
    col_marian, col_emily, col_valen, col_sofi = st.columns(4)
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
