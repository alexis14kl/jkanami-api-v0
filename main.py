from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

# Establecer opciones de Chrome
chrome_options = Options()
chrome_options.add_argument('--headless')  # Ejecutar Chrome sin cabeza
chrome_options.add_argument('--no-sandbox')  # Evitar problemas en entornos sin cabeza
chrome_options.add_argument('--disable-dev-shm-usage')  # Solucionar errores de memoria
chrome_options.add_argument('----disable-gpu')
chrome_options.add_argument('--remote-debugging-port=9222')  # Puerto para depuración remota

# Especifica el servicio y el path del driver
chrome_service = Service(executable_path="/app/.heroku/chrome/bin/google-chrome")

# Iniciar el navegador
driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

# Accede a la página deseada
driver.get("https://jkanime.net/dragon-ball-gt/16/")

# Espera un poco para asegurarse de que la página se cargue
driver.implicitly_wait(10)

# Verifica si la página se ha cargado correctamente (comprobando el título)
if "Dragon Ball GT" in driver.title:
    print("La página se cargó correctamente")
else:
    print("La página no se cargó correctamente")

# Cierra el navegador
driver.quit()
