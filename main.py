import re
import time
from fastapi import FastAPI
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import os

# Crear una instancia de FastAPI
app = FastAPI()

# Asumiendo que estas variables están configuradas en Heroku o de alguna otra forma
GOOGLE_CHROME_PATH = os.getenv("GOOGLE_CHROME_PATH", "/app/.apt/usr/bin/google_chrome")
CHROMEDRIVER_PATH = os.getenv("CHROMEDRIVER_PATH", "/app/.chromedriver/bin/chromedriver")

def configurar_navegador():
    # Crear opciones para el navegador
    chrome_options = Options()
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.binary_location = GOOGLE_CHROME_PATH

    # Usar el servicio para el ChromeDriver
    service = Service(executable_path=CHROMEDRIVER_PATH)
    
    # Crear una instancia del navegador con las opciones y servicio
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

@app.get("/")
def read_root():
    return {"message": "¡Hola, FastAPI!"}
