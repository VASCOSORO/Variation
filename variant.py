import streamlit as st
import requests

# URL de la API de Node.js expuesta por ngrok o localhost
API_URL = "http://localhost:3000"  # Cambia esto por la URL de ngrok si lo estás usando

# Lista de vendedoras y etapas
vendedoras = ['Marian', 'Emily', 'Valen', 'Sofi']
etapas = ['Ingreso Nuevo', 'En Charla', 'Agregando Productos', 'Esperando Pago', 'Pedido Enviado', 'SandBox']

# Inicializar el estado de asignaciones en session_state
if 'asignaciones' not in st.session_state:
    st.session_state.asignaciones = {vendedora: {etapa: [] for etapa in etapas} for vendedora in vendedoras}

# Inicializar el estado de mensajes_pileta en session_state
if 'mensajes_pileta' not in st.session_state:
    st.session_state.mensajes_pileta = []

# Función para obtener mensajes desde la API
def obtener_mensajes():
    try:
        response = requests.get(f"{API_URL}/mensajes")
        response.raise_for_status()  # Verifica si la respuesta es 200 OK
        mensajes = response.json()
        st.session_state.mensajes_pileta = mensajes  # Actualiza los mensajes en session_state
    except requests.exceptions.RequestException as e:
        st.error(f"No se pudo conectar con la API: {e}")
    except ValueError:
        st.error("La API devolvió una respuesta no válida (no es JSON).")

# Obtener los mensajes al cargar la aplicación
obtener_mensajes()

# Función para asignar mensaje a una vendedora
def asignar_mensaje(mensaje, vendedora_seleccionada):
    # Añadir el mensaje a la etapa 'Ingreso Nuevo' de la vendedora seleccionada
    st.session_state.asignaciones[vendedora_seleccionada]['Ingreso Nuevo'].append(mensaje)
    # Eliminar el mensaje de la pileta
    st.session_state.mensajes_pileta = [m for m in st.session_state.mensajes_pileta if m['id'] != mensaje['id']]
    st.success(f"Mensaje asignado a {vendedora_seleccionada}")

# Barra de navegación superior
st.markdown("""
    <style>
        .navbar {
            background-color: #343a40;
            color: #fff;
            padding: 10px 20px;
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            display: flex;
            justify-content: space-between;
            align-items: center;
            height: 60px;
            z-index: 1000;
        }
        .main-content {
            margin-top: 80px;
        }
    </style>
    <div class="navbar">
        <h1>CRM Dashboard</h1>
        <div>Bienvenido, Usuario</div>
    </div>
""", unsafe_allow_html=True)

# Contenedor principal
st.markdown('<div class="main-content">', unsafe_allow_html=True)

# Diseño de la interfaz
col_pileta, col_marian, col_emily, col_valen, col_sofi = st.columns([2, 1, 1, 1, 1])

# Pileta de Mensajes
with col_pileta:
    st.header("Pileta de Mensajes")
    if st.session_state.mensajes_pileta:
        for idx, mensaje in enumerate(st.session_state.mensajes_pileta):
            st.markdown("---")
            col1, col2 = st.columns([1, 3])
            
            with col1:
                # Imagen de perfil o imagen predeterminada
                imagen_url = mensaje.get('imagen', "https://via.placeholder.com/50")
                st.image(imagen_url, width=50)
                st.markdown(f"**{mensaje['numero']}**")
            
            with col2:
                st.markdown(f"**{mensaje['mensaje']}**")
                vendedora_seleccionada = st.selectbox('Asignar a:', vendedoras, key=f"select_{idx}")
            
            # Botón para asignar
            if st.button(f"Asignar a {vendedora_seleccionada}", key=f"asignar_{idx}"):
                asignar_mensaje(mensaje, vendedora_seleccionada)
    else:
        st.info("No hay mensajes en la pileta.")

# Función para mostrar las asignaciones de cada vendedora
def mostrar_vendedora(vendedora):
    st.subheader(f"Solapa de {vendedora}")
    columnas = st.columns(len(etapas))
    for idx, etapa in enumerate(etapas):
        with columnas[idx]:
            st.markdown(f"### {etapa}")
            mensajes_etapa = st.session_state.asignaciones[vendedora][etapa]
            if mensajes_etapa:
                for msg_idx, mensaje in enumerate(mensajes_etapa):
                    if st.button(f"Ver chat {mensaje['numero']} - {msg_idx}", key=f"chat_{vendedora}_{etapa}_{msg_idx}"):
                        st.session_state.view = 'chat'
                        st.session_state.mensaje_chat = mensaje
                        st.session_state.vendedora_chat = vendedora
                        st.session_state.etapa_chat = etapa
            else:
                st.write("No hay mensajes en esta etapa.")

# Mostrar módulos de cada vendedora
with col_marian:
    mostrar_vendedora('Marian')

with col_emily:
    mostrar_vendedora('Emily')

with col_valen:
    mostrar_vendedora('Valen')

with col_sofi:
    mostrar_vendedora('Sofi')

# Vista de Chat
if 'view' in st.session_state and st.session_state.view == 'chat':
    mensaje = st.session_state.get('mensaje_chat', {})
    vendedora = st.session_state.get('vendedora_chat', '')
    etapa = st.session_state.get('etapa_chat', '')
    
    st.markdown("---")
    st.header(f"Chat con {mensaje.get('nombre', mensaje.get('numero', 'Desconocido'))} ({etapa})")
    
    # Mostrar mensajes (esto es estático, puedes mejorar para mostrar el historial)
    st.text_area("Chat", value=f"Mensajes enviados y recibidos con {mensaje['numero']}", height=300)
    
    # Datos del contacto
    st.subheader(f"Datos de {mensaje['numero']}")
    st.write(f"**Nombre:** {mensaje.get('nombre', 'Desconocido')}")
    st.write(f"**Estado:** {mensaje.get('estado', 'Desconocido')}")
    st.write(f"**Imagen de perfil:** {mensaje.get('imagen', 'No disponible')}")
    
    # Inputs para enviar un nuevo mensaje (funcionalidad futura)
    st.text_input("Escribe un mensaje")
    st.file_uploader("Adjuntar archivo", type=['png', 'jpg', 'pdf'])
    
    # Botón para enviar un nuevo mensaje
    if st.button("Enviar"):
        st.success(f"Mensaje enviado a {mensaje['numero']}")
        # Aquí puedes agregar la lógica para enviar el mensaje a través de tu backend
    
    # Cambiar etapa del cliente
    nueva_etapa = st.selectbox("Cambiar etapa a:", etapas, index=etapas.index(etapa))
    if nueva_etapa != etapa:
        # Mover el mensaje a la nueva etapa
        st.session_state.asignaciones[vendedora][etapa].remove(mensaje)
        st.session_state.asignaciones[vendedora][nueva_etapa].append(mensaje)
        st.session_state.etapa_chat = nueva_etapa
        st.success(f"Etapa cambiada a {nueva_etapa}")
    
    # Reasignar a otro usuario
    nuevo_usuario = st.selectbox("Reasignar a:", vendedoras, index=vendedoras.index(vendedora))
    if nuevo_usuario != vendedora:
        # Mover el mensaje a la nueva vendedora y a la etapa 'Ingreso Nuevo'
        st.session_state.asignaciones[vendedora][etapa].remove(mensaje)
        st.session_state.asignaciones[nuevo_usuario]['Ingreso Nuevo'].append(mensaje)
        st.session_state.vendedora_chat = nuevo_usuario
        st.session_state.etapa_chat = 'Ingreso Nuevo'
        st.success(f"Reasignado a {nuevo_usuario}")
    
    # Botón para volver a la solapa principal
    if st.button("Volver a la Solapa"):
        st.session_state.view = 'pileta'

# Cierre del contenedor principal
st.markdown('</div>', unsafe_allow_html=True)
