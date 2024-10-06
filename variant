import streamlit as st
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

# Función para enviar un mensaje a través de WhatsApp Web usando Selenium
def enviar_mensaje(contacto, mensaje):
    # Inicializamos el driver de Chrome (asegúrate de que el path de chromedriver sea correcto)
    driver = webdriver.Chrome(executable_path='./chromedriver')  # Cambia el path según la ubicación de chromedriver
    driver.get('https://web.whatsapp.com')

    # Esperamos a que el usuario escanee el código QR
    st.info("Escanea el código QR de WhatsApp Web y presiona Enter en la terminal.")
    input("Escaneá el código QR y presioná Enter...")

    # Buscar el contacto en WhatsApp
    search_box = driver.find_element_by_xpath('//div[@contenteditable="true"][@data-tab="3"]')
    search_box.click()
    search_box.send_keys(contacto)
    search_box.send_keys(Keys.ENTER)

    # Esperamos un poco para que cargue el chat
    time.sleep(2)

    # Enviar el mensaje
    message_box = driver.find_element_by_xpath('//div[@contenteditable="true"][@data-tab="6"]')
    message_box.click()
    message_box.send_keys(mensaje)
    message_box.send_keys(Keys.ENTER)

    # Esperamos y cerramos el navegador
    time.sleep(2)
    driver.quit()

# Interfaz de usuario en Streamlit
st.title("Automatización de WhatsApp con Selenium")

# Campos para ingresar el contacto y el mensaje
contacto = st.text_input("Nombre del contacto o número (incluye el código de país):")
mensaje = st.text_area("Mensaje a enviar:")

# Botón para enviar el mensaje
if st.button("Enviar mensaje"):
    if contacto and mensaje:
        enviar_mensaje(contacto, mensaje)
        st.success(f"Mensaje enviado a {contacto}")
    else:
        st.error("Por favor, completá los campos de contacto y mensaje.")
