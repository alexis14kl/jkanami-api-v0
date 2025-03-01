import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

# Configurar las opciones de Chrome
op = Options()

# Especifica la ubicación del ejecutable de Google Chrome
op.binary_location = os.environ.get("GOOGLE_CHROME_BIN")

# Añade un argumento para desactivar la interfaz de usuario del navegador
op.add_argument("--disable-dev-shm-usage")
op.add_argument("--no-sandbox")

# Configura la ubicación del chromedriver utilizando Service
chromedriver_path = os.environ.get("CHROMEDRIVER_PATH")
service = Service(chromedriver_path)

# Inicia el controlador de Chrome
driver = webdriver.Chrome(service=service, options=op)

# Accede a la página deseada
driver.get("https://jkanime.net/dragon-ball-gt/16/")

# Espera un poco para asegurarse de que la página se cargue
driver.implicitly_wait(10)  # Espera hasta 10 segundos para que cargue

# Verifica si la página se ha cargado correctamente (comprobando el título)
if "Dragon Ball GT" in driver.title:
    print("La página se cargó correctamente")
else:
    print("La página no se cargó correctamente")

# Cierra el navegador
driver.quit()
