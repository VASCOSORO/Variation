import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time

# Lista de clientes inicial (simulación de una base de datos simple)
clientes = [
    {"nombre": "Juan Pérez", "telefono": "+5491112345678", "email": "juan@example.com"},
    {"nombre": "Ana Gómez", "telefono": "+5491122334455", "email": "ana@example.com"},
]

# Función para iniciar WhatsApp Web y enviar mensaje
def enviar_mensaje(contacto, mensaje):
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")

    # Configurar el servicio de ChromeDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # Acceder a WhatsApp Web
    driver.get('https://web.whatsapp.com')

    # Esperar a que el usuario escanee el código QR
    st.info("Escanea el código QR de WhatsApp Web.")
    while True:
        try:
            driver.find_element(By.XPATH, '//div[@id="side"]')  # Detecta si la sesión está iniciada
            st.success("Sesión de WhatsApp conectada.")
            break
        except:
            time.sleep(2)  # Espera antes de volver a verificar

    # Buscar el contacto en WhatsApp
    search_box = driver.find_element(By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]')
    search_box.click()
    search_box.send_keys(contacto)
    search_box.send_keys(Keys.ENTER)

    # Enviar el mensaje
    time.sleep(2)
    message_box = driver.find_element(By.XPATH, '//div[@contenteditable="true"][@data-tab="6"]')
    message_box.click()
    message_box.send_keys(mensaje)
    message_box.send_keys(Keys.ENTER)

    # Cerrar el navegador
    time.sleep(2)
    driver.quit()

# Interfaz principal del CRM
st.title("CRM de Clientes con WhatsApp")

# Mostrar lista de clientes
st.subheader("Lista de clientes")
for cliente in clientes:
    st.write(f"Nombre: {cliente['nombre']}")
    st.write(f"Teléfono: {cliente['telefono']}")
    st.write(f"Email: {cliente['email']}")
    if st.button(f"Enviar mensaje a {cliente['nombre']}"):
        mensaje = st.text_area(f"Escribí el mensaje para {cliente['nombre']}")
        if st.button("Enviar mensaje"):
            enviar_mensaje(cliente['telefono'], mensaje)

# Agregar un nuevo cliente
st.subheader("Agregar nuevo cliente")
with st.form(key="form_nuevo_cliente"):
    nuevo_nombre = st.text_input("Nombre")
    nuevo_telefono = st.text_input("Teléfono")
    nuevo_email = st.text_input("Email")
    submit_button = st.form_submit_button("Agregar cliente")

    if submit_button:
        nuevo_cliente = {"nombre": nuevo_nombre, "telefono": nuevo_telefono, "email": nuevo_email}
        clientes.append(nuevo_cliente)
        st.success(f"Cliente {nuevo_nombre} agregado con éxito.")
