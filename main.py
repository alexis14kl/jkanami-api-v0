from fastapi import FastAPI
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from fastapi.responses import JSONResponse
import os
import time

# Crear la instancia de la aplicación FastAPI
app = FastAPI()

# Función para configurar el navegador (con opciones headless)
def configurar_navegador():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Ejecutar en modo headless (sin interfaz gráfica)
    chrome_options.add_argument("--no-sandbox")  # Necesario para algunos entornos como Heroku
    chrome_options.add_argument("--disable-dev-shm-usage")  # Desactivar memoria compartida
    chrome_options.add_argument("--disable-gpu")  # Desactivar el uso de GPU (no necesario en modo headless)
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN", "/app/.apt/usr/bin/google-chrome")
    driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH", "/app/.chromedriver/bin/chromedriver"), options=chrome_options)
    return driver

# Función para obtener el título del episodio desde la URL proporcionada
def obtener_titulo_episodio(driver, url):
    # Acceder a la página principal
    driver.get(url)

    # Esperar a que la página cargue completamente
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "h1.mb-2")))
    except Exception as e:
        return {"error": f"Error al esperar el elemento: {str(e)}"}

    try:
        # Buscar el título del episodio dentro del <h1> con la clase mb-2
        titulo = driver.find_element(By.CSS_SELECTOR, "h1.mb-2").text
        return {"titulo": titulo}
    except Exception as e:
        return {"error": f"No se encontró el título del episodio: {str(e)}"}

# Ruta de la API para obtener el título del episodio
@app.get("/get-episodio-titulo/")
async def get_episodio_titulo(url: str):  # Recibir la URL como parámetro de consulta
    # Configurar el navegador
    driver = configurar_navegador()

    # Obtener el título del episodio
    response = obtener_titulo_episodio(driver, url)

    # Cerrar el navegador después de la ejecución
    driver.quit()

    # Retornar la respuesta
    return response
