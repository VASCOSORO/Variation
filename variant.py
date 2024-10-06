import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time

# Función para conectar a WhatsApp Web y aplicar colores a los chats
def iniciar_whatsapp_y_aplicar_colores(clientes):
    # Configurar opciones de Chrome
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")  # Asegurar que el navegador se abre maximizado
    chrome_options.add_argument("--headless")  # Ejecutar en modo sin interfaz gráfica (opcional)
    chrome_options.add_argument("--disable-gpu")  # Necesario para algunos entornos en headless mode
    chrome_options.add_argument("--no-sandbox")  # Evitar problemas en algunos entornos de servidor

    # Configuramos el servicio de ChromeDriver con webdriver_manager
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
            time.sleep(2)  # Esperar antes de volver a verificar

    # Aplicar colores personalizados a los chats según los clientes
    for cliente in clientes:
        # Usar un identificador para buscar el chat del cliente en la interfaz de WhatsApp Web
        try:
            search_box = driver.find_element(By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]')
            search_box.click()
            search_box.send_keys(cliente['telefono'])
            search_box.send_keys(Keys.ENTER)

            # Aplicar color personalizado al chat del cliente
            script = f"""
            var chat = document.querySelectorAll('div[role="region"]');
            for (var i = 0; i < chat.length; i++) {{
                chat[i].style.backgroundColor = "{cliente['color']}";
            }}
            """
            driver.execute_script(script)
            st.success(f"Aplicado color {cliente['color']} al chat de {cliente['nombre']}")
        except:
            st.error(f"No se pudo encontrar el chat de {cliente['nombre']}.")

# Lista de clientes con colores personalizados
clientes = [
    {"nombre": "Juan Pérez", "telefono": "+5491112345678", "color": "#FFCCCC"},
    {"nombre": "Ana Gómez", "telefono": "+5491122334455", "color": "#CCFFCC"},
    {"nombre": "Carlos Díaz", "telefono": "+5491133445566", "color": "#CCCCFF"}
]

# Interfaz de usuario en Streamlit para el CRM
st.title("CRM con WhatsApp y Colores Personalizados")

# Botón para iniciar WhatsApp y aplicar colores
if st.button("Iniciar WhatsApp y aplicar colores"):
    iniciar_whatsapp_y_aplicar_colores(clientes)
