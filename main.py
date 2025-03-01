import re
import time
from fastapi import FastAPI
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import os

# Crear una instancia de FastAPI
app = FastAPI()

# Asumiendo que estas variables están configuradas en Heroku o de alguna otra forma
GOOGLE_CHROME_PATH = os.getenv("GOOGLE_CHROME_PATH", "/app/.apt/usr/bin/google_chrome")
CHROMEDRIVER_PATH = os.getenv("CHROMEDRIVER_PATH", "/app/.chromedriver/bin/chromedriver")

def configurar_navegador():
    # Crear opciones para el navegador
    chrome_options = Options()
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.binary_location = GOOGLE_CHROME_PATH

    # Usar el servicio para el ChromeDriver
    service = Service(executable_path=CHROMEDRIVER_PATH)
    
    # Crear una instancia del navegador con las opciones y servicio
    driver = webdriver.Chrome(service=service, options=chrome_options)
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
    except Exception as e:
        return {"error": f"No se encontró el iframe adecuado: {str(e)}"}

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
