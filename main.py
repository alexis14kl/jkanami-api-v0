import os
from selenium import webdriver

# Configurar las opciones de Chrome
op = webdriver.ChromeOptions()

# Especifica la ubicación del ejecutable de Google Chrome
op.binary_location = os.environ.get("GOOGLE_CHROME_BIN")

# Añade un argumento para desactivar la interfaz de usuario del navegador
op.add_argument("--disable-dev-shm-usage")

# Aquí se pasa la ubicación del controlador de Chrome (chromedriver)
driver = webdriver.Chrome(executable_path=os.environ.get("CROMEDRIVER_PATH"), options=op)

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

