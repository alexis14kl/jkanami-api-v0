from fastapi import FastAPI
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from fastapi.responses import JSONResponse

# Crear la instancia de la aplicación FastAPI
app = FastAPI()

# Función que ejecuta el Selenium
def get_selenium_data():
    # Configurar las opciones de Chrome para modo headless
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Asegura que Chrome se ejecute en modo headless
    chrome_options.add_argument("--no-sandbox")  # Necesario para algunos entornos como Heroku
    chrome_options.add_argument("--disable-dev-shm-usage")  # Desactivar memoria compartida
    chrome_options.add_argument("--disable-gpu")  # Desactivar el uso de GPU (no necesario en modo headless)

    # Crear el objeto WebDriver
    driver = webdriver.Chrome(options=chrome_options)

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
