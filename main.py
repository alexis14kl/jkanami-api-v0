import re
import time
from fastapi import FastAPI
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

# Crear una instancia de FastAPI
app = FastAPI()

def configurar_navegador():
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # Ejecutar Chrome en modo headless
    chrome_options.add_argument('--disable-gpu')  # Deshabilitar la aceleración de GPU (útil para headless)
    chrome_options.add_argument('--no-sandbox')  # Evitar errores en entorno sin entorno gráfico
    chrome_options.add_argument('--remote-debugging-port=9222')  # Configurar puerto de depuración remoto
    chrome_options.add_argument('--disable-dev-shm-usage')  # Solución a problemas de memoria compartida en algunos entornos (como Heroku)

    # Usar Chromium en vez de Chrome
    chrome_options.binary_location = '/usr/bin/chromium'

    # Ejecutar el navegador con las opciones configuradas
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    return driver


def obtener_m3u8_link(driver, url):
    # Acceder a la página principal
    driver.get(url)

    # Esperar a que la página cargue completamente
    time.sleep(5)  # Ajusta el tiempo si es necesario (espera a que cargue el video)
    
    # Cambiar al iframe que contiene el reproductor
    try:
        iframe = driver.find_element(By.CLASS_NAME, "player_conte")
        driver.switch_to.frame(iframe)
    except:
        return {"error": "No se encontró el iframe adecuado."}

    # Obtener el código fuente dentro del iframe
    iframe_html = driver.page_source

    # Buscar el script que contiene 'var parts =' con una expresión regular
    match = re.search(r"var\s+parts\s*=\s*{[^}]*?swarmId\s*:\s*'([^']+\.m3u8)'", iframe_html)

    if match:
        # Si encontramos la URL, la retornamos
        m3u8_url = match.group(1)
        return {"m3u8_url": m3u8_url}
    else:
        return {"error": "No se encontró el enlace m3u8 dentro del iframe."}

@app.get("/get-m3u8/")
async def get_m3u8_link(url: str):  # Aquí cambiamos para recibir el parámetro en la query string
    # Configurar el navegador
    driver = configurar_navegador()

    # Obtener la URL del m3u8
    response = obtener_m3u8_link(driver, url)

    # Cerrar el navegador después de la ejecución
    driver.quit()

    # Retornar la respuesta
    return response

@app.get("/")
def read_root():
    return {"message": "¡Hola, FastAPI!"}
