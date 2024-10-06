from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

# Función para enviar un mensaje a través de WhatsApp Web usando Selenium
def enviar_mensaje(contacto, mensaje):
    # Configuramos el servicio de ChromeDriver con webdriver_manager
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)

    driver.get('https://web.whatsapp.com')

    # Esperamos a que el usuario escanee el código QR
    input("Escaneá el código QR en WhatsApp Web y presioná Enter...")

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
