# pip install fastapi uvicorn
from typing import Union
from fastapi import FastAPI
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


# Specify the driver version compatible with the version of Chrome

app = FastAPI()

def configurar_navegador():
    options = Options()
    chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    return driver

def obtener_m3u8_link(driver, url):
    driver.get(url)
    
    try:
        # Espera explícita hasta que el iframe esté disponible
        iframe = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "player_conte"))
        )
        driver.switch_to.frame(iframe)

        iframe_html = driver.page_source
        match = re.search(r"var\s+parts\s*=\s*{[^}]*?swarmId\s*:\s*'([^']+\.m3u8)'", iframe_html)

        if match:
            return match.group(1)
        else:
            return None

    except Exception as e:
        return f"Error al obtener el enlace m3u8: {str(e)}"

@app.get("/get_m3u8/")
def get_m3u8(url: str):
    driver = configurar_navegador()
    m3u8_url = obtener_m3u8_link(driver, url)
    driver.quit()

    if m3u8_url:
        return {"m3u8_url": m3u8_url}
    else:
        return {"error": "No se encontró el enlace m3u8 en la página proporcionada."}

@app.get("/")
def read_root():
    return {"Hello": "Estás conectado"}

# ejecutar api
# uvicorn main:app --reload


#heroku buildpacks:add https://github.com/heroku/heroku-buildpack-chrome-for-testing --app jkanami-api-v0
