from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def get_selenium_data():
    # Configurar las opciones de Chrome para modo headless
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Asegura que Chrome se ejecute en modo headless
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")

    # Crear el objeto WebDriver
    driver = webdriver.Chrome(options=chrome_options)

    # Acceder a la página
    driver.get("https://www.selenium.dev/selenium/web/web-form.html")

    # Esperar hasta que el h1 esté presente (espera explícita)
    try:
        h1_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.col-12 h1.display-6"))
        )
        h1_text = h1_element.text  # Obtener el texto del h1
    except Exception as e:
        driver.quit()
        return {"error": f"No se encontró el h1: {str(e)}"}

    # Cerrar el navegador
    driver.quit()

    return {"h1_text": h1_text}
