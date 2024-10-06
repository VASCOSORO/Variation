import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time

# Función para enviar un mensaje a través de WhatsApp Web usando Selenium
def enviar_mensaje(contacto, mensaje):
    # Configuramos el servicio de ChromeDriver con webdriver_manager
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)

    # Acceder a WhatsApp Web
    driver.get('https://web.whatsapp.com')

    # Esperamos hasta que el usuario haya escaneado el código QR
    st.info("Escanea el código QR de WhatsApp Web y espera a que se conecte.")
    while True:
        try:
            # Comprobar si la sesión de WhatsApp ha sido iniciada correctamente
            driver.find_element(By.XPATH, '//div[@id="side"]')
            st.success("Sesión de WhatsApp conectada.")
            break
        except:
            time.sleep(2)  # Esperar antes de volver a comprobar si se ha iniciado la sesión

    # Buscar el contacto en WhatsApp
    search_box = driver.find_element(By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]')
    search_box.click()
    search_box.send_keys(contacto)
    search_box.send_keys(Keys.ENTER)

    # Esperamos un poco para que cargue el chat
    time.sleep(2)

    # Enviar el mensaje
    message_box = driver.find_element(By.XPATH, '//div[@contenteditable="true"][@data-tab="6"]')
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
