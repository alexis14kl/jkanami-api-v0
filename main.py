from fastapi import FastAPI
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from fastapi.responses import JSONResponse
import tempfile
import os

# Crear la instancia de la aplicación FastAPI
app = FastAPI()

# Función que ejecuta el Selenium
def get_selenium_data():
    # Configurar las opciones de Chrome para modo headless
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")  # Necesario para algunos entornos como Heroku
    chrome_options.add_argument("--disable-dev-shm-usage")  # Desactivar memoria compartida
    chrome_options.add_argument("--disable-gpu")  # Desactivar el uso de GPU (no necesario en modo headless)

    # Crear un directorio temporal único para el perfil de usuario
    user_data_dir = tempfile.mkdtemp()  # Crear un directorio temporal
    chrome_options.add_argument(f"--user-data-dir={user_data_dir}")  # Usar el directorio temporal como perfil de usuario


    # Crear el objeto WebDriver
    driver = webdriver.Chrome(options=chrome_options)
    

    # Acceder a la página
    driver.get("https://www.selenium.dev/selenium/web/web-form.html")

    # Esperar un poco para asegurarse de que los elementos estén cargados
    driver.implicitly_wait(0.5)

    # Buscar el h1 dentro del div con la clase "col-12"
    try:
        h1_element = driver.find_element(by=By.CSS_SELECTOR, value="div.col-12 h1.display-6")
        h1_text = h1_element.text  # Obtener el texto del h1
    except Exception as e:
        return {"error": f"No se encontró el h1: {str(e)}"}

    # Cerrar el navegador
    driver.quit()

    # Retornar el resultado
    return {"h1_text": h1_text}

# Ruta de la API que ejecuta Selenium
@app.get("/run_selenium")
async def run_selenium():
    try:
        result = get_selenium_data()  # Ejecutar el código de Selenium
        return JSONResponse(content=result)  # Retornar el resultado como JSON
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
