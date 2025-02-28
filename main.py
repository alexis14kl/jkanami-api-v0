import re
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

def configurar_navegador():
    # Configuración de las opciones de Chrome para ejecutar sin interfaz gráfica
    options = Options()
    options.add_argument("--headless")  # Ejecutar Chrome sin interfaz gráfica
    options.add_argument("--disable-gpu")  # Desactivar la GPU para mejorar el rendimiento
    options.add_argument("--no-sandbox")  # Evitar errores en entornos limitados como Heroku
    options.add_argument("--disable-software-rasterizer")  # Desactivar el renderizado de software
    options.add_argument("--remote-debugging-port=9222")  # Usar puerto de depuración remoto, útil en entornos como Heroku

    # Iniciar el navegador Chrome con las opciones configuradas
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver

def obtener_m3u8_link(driver, url):
    try:
        # Acceder a la página proporcionada
        driver.get(url)

        # Esperar un momento para asegurarse de que la página se haya cargado
        time.sleep(5)  # Ajusta el tiempo si es necesario

        # Cambiar al iframe que contiene el reproductor
        iframe = driver.find_element(By.CLASS_NAME, "player_conte")
        driver.switch_to.frame(iframe)

        # Obtener el código fuente del iframe
        iframe_html = driver.page_source

        # Buscar el enlace m3u8 utilizando una expresión regular
        match = re.search(r"var\s+parts\s*=\s*{[^}]*?swarmId\s*:\s*'([^']+\.m3u8)'", iframe_html)

        if match:
            # Si se encuentra un enlace m3u8, devolverlo
            m3u8_url = match.group(1)
            return m3u8_url
        else:
            # Si no se encuentra el enlace m3u8
            return None
    except Exception as e:
        return f"Error al obtener el enlace m3u8: {str(e)}"

def main(url):
    # Configurar el navegador
    driver = configurar_navegador()

    # Obtener el enlace m3u8 de la página
    m3u8_url = obtener_m3u8_link(driver, url)

    # Cerrar el navegador después de la ejecución
    driver.quit()

    if m3u8_url:
        return m3u8_url
    else:
        return "No se encontró el enlace m3u8 en la página proporcionada."

if __name__ == "__main__":
    # Puedes pasar la URL que deseas procesar aquí
    url = "https://www.ejemplo.com"  # Cambia esta URL a la URL que necesites

    # Ejecutar la función principal
    resultado = main(url)
    print(f"Resultado: {resultado}")
