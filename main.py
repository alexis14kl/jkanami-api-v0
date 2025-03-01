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
    chrome_options.add_argument("--remote-debugging-port=9222")  # Usar un puerto de depuración remoto
    chrome_options.add_argument("--disable-software-rasterizer")  # Desactivar rasterización de software

    # Crear el objeto WebDriver
    try:
        driver = webdriver.Chrome(options=chrome_options)
    except Exception as e:
        return {"error": f"Error al iniciar el navegador: {str(e)}"}

    # Acceder a la página
    driver.get("https://jkanime.net/")

    # Esperar un poco para asegurarse de que los elementos estén cargados
    driver.implicitly_wait(0.5)

    # Buscar el h1 dentro del div con la clase "col-12"
    try:
        h1_element = driver.find_element(by=By.CSS_SELECTOR, value="div.section-title h5")
        h1_text = h1_element.text  # Obtener el texto del h1
    except Exception as e:
        return {"error": f"No se encontró el h1: {str(e)}"}

    # Cerrar el navegador
    driver.quit()

    # Retornar el resultado
    return {"h1_text": h1_text}

# Ruta de la API que ejecuta Selenium
@app.get("/")
async def run_selenium():
    try:
        result = get_selenium_data()  # Ejecutar el código de Selenium
        return JSONResponse(content=result)  # Retornar el resultado como JSON
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
