from fastapi import FastAPI
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from fastapi.responses import JSONResponse
import time
import re

# Crear la instancia de la aplicación FastAPI
app = FastAPI()

# Función que ejecuta el Selenium
def obtener_m3u8_link(driver, url):
    # Acceder a la página principal
    driver.get(url)

    # Esperar a que la página cargue completamente
    time.sleep(5)  # Ajusta el tiempo si es necesario (espera a que cargue el video)

    # Cambiar al iframe que contiene el reproductor
    iframe = driver.find_element(By.CLASS_NAME, "player_conte")
    driver.switch_to.frame(iframe)

    # Obtener el código fuente dentro del iframe
    iframe_html = driver.page_source

    # Buscar el script que contiene 'var parts =' con una expresión regular
    match = re.search(r"var\s+parts\s*=\s*{[^}]*?swarmId\s*:\s*'([^']+\.m3u8)'", iframe_html)

    if match:
        # Si encontramos la URL, la retornamos
        m3u8_url = match.group(1)
        print(f"Enlace m3u8 encontrado: {m3u8_url}")
        return m3u8_url
    else:
        print("No se encontró el enlace m3u8 dentro del iframe.")
        return None

# Función para configurar el navegador (con opciones headless)
def configurar_navegador():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Ejecutar en modo headless (sin interfaz gráfica)
    chrome_options.add_argument("--no-sandbox")  # Necesario para algunos entornos como Heroku
    chrome_options.add_argument("--disable-dev-shm-usage")  # Desactivar memoria compartida
    chrome_options.add_argument("--disable-gpu")  # Desactivar el uso de GPU (no necesario en modo headless)
    driver = webdriver.Chrome(options=chrome_options)
    return driver

# Ruta de la API que ejecuta Selenium para múltiples URLs
@app.get("/run_selenium")
async def run_selenium(urls: list[str]):
    # Verificar que se recibieron URLs
    if not urls:
        return JSONResponse(status_code=400, content={"error": "No URLs provided."})
    
    # Configurar el navegador
    driver = configurar_navegador()

    # Almacenar los resultados de las URLs procesadas
    results = {}

    for url in urls:
        try:
            m3u8_url = obtener_m3u8_link(driver, url)
            if m3u8_url:
                results[url] = {"m3u8_url": m3u8_url}
            else:
                results[url] = {"error": "No m3u8 link found"}
        except Exception as e:
            results[url] = {"error": str(e)}
    
    # Cerrar el navegador después de la ejecución
    driver.quit()

    # Retornar los resultados en formato JSON
    return JSONResponse(content=results)

