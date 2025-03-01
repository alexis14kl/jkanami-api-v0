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

    # Acceder a la página
    driver.get("https://www.selenium.dev/selenium/web/web-form.html")

    # Obtener el título de la página (por si necesitas usarlo)
    title = driver.title

    # Esperar un poco para asegurarse de que los elementos estén cargados
    driver.implicitly_wait(0.5)

    # Localizar los elementos y realizar la interacción
    text_box = driver.find_element(by=By.NAME, value="my-text")
    submit_button = driver.find_element(by=By.CSS_SELECTOR, value="button")

    text_box.send_keys("Selenium")
    submit_button.click()

    # Obtener el mensaje que aparece después de enviar el formulario
    message = driver.find_element(by=By.ID, value="message")
    text = message.text

    # Cerrar el navegador
    driver.quit()

    # Retornar el resultado
    return text

# Ruta de la API que ejecuta Selenium
@app.get("/run_selenium")
async def run_selenium():
    try:
        result = get_selenium_data()  # Ejecutar el código de Selenium
        return JSONResponse(content={"message": result})  # Retornar el resultado como JSON
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

