# pip install fastapi uvicorn

# ejecutar api
# uvicorn main:app --reload


from typing import Union
from fastapi import FastAPI
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time

app = FastAPI()

# Configurar el navegador en modo headless
def configurar_navegador():
    options = Options()
    options.add_argument("--headless")  # Ejecutar en modo headless
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver

# Función para obtener el link m3u8
def obtener_m3u8_link(driver, url):
    driver.get(url)
    time.sleep(5)  # Agregar un pequeño retraso para que la página se cargue correctamente

    # Encontrar el iframe y cambiar el contexto
    iframe = driver.find_element(By.CLASS_NAME, "player_conte")
    driver.switch_to.frame(iframe)

    # Obtener el código HTML del iframe y buscar el link m3u8
    iframe_html = driver.page_source
    match = re.search(r"var\s+parts\s*=\s*{[^}]*?swarmId\s*:\s*'([^']+\.m3u8)'", iframe_html)

    if match:
        return match.group(1)
    else:
        return None

# Ruta para obtener el enlace m3u8
@app.get("/get_m3u8/")
def get_m3u8(url: str):
    driver = configurar_navegador()
    m3u8_url = obtener_m3u8_link(driver, url)
    driver.quit()

    if m3u8_url:
        return {"m3u8_url": m3u8_url}
    else:
        return {"error": "No se encontró el enlace m3u8 en la página proporcionada."}

# Ruta de prueba
@app.get("/")
def read_root():
    return {"Hello": "Estás conectado"}

