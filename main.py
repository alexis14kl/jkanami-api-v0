# pip install fastapi uvicorn
from typing import Union
from fastapi import FastAPI
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time

app = FastAPI()

def configurar_navegador():
    options = Options()
    options.add_argument("window-size=1x1")
    options.add_argument("--no-sandbox")  
    options.add_argument("--disable-extensions")  
    options.add_argument("--disable-sync")  
    options.add_argument("--no-first-run")  
    options.add_argument("--disable-gpu")  
    options.add_argument("--disable-software-rasterizer")  
    options.add_argument("--disable-images")  
    options.add_argument("window-size=1x1")  
    # Agregar modo headless para que el navegador no se abra visualmente
    options.add_argument("--headless")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver

def obtener_m3u8_link(driver, url):
    driver.get(url)
    time.sleep(5)

    iframe = driver.find_element(By.CLASS_NAME, "player_conte")
    driver.switch_to.frame(iframe)

    iframe_html = driver.page_source
    match = re.search(r"var\s+parts\s*=\s*{[^}]*?swarmId\s*:\s*'([^']+\.m3u8)'", iframe_html)

    if match:
        return match.group(1)
    else:
        return None

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
    return {"Hello": "Estas conectado"}
# ejecutar api
# uvicorn main:app --reload


