# pip install fastapi uvicorn
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

app = FastAPI()

def configurar_navegador():
    # Create a Chrome options instance
    options = Options()
    options.add_argument('--headless')  # Run Chrome in headless mode (without GUI)
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    # Initialize the Chrome driver with the specified options
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver

def obtener_m3u8_link(driver, url):
    driver.get(url)
    
    try:
        # Wait explicitly for the iframe to be available
        iframe = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "player_conte"))
        )
        driver.switch_to.frame(iframe)

        iframe_html = driver.page_source
        # Search for the m3u8 link within the iframe's HTML source
        match = re.search(r"var\s+parts\s*=\s*{[^}]*?swarmId\s*:\s*'([^']+\.m3u8)'", iframe_html)

        if match:
            return match.group(1)  # Return the m3u8 link found
        else:
            return None  # Return None if no match is found

    except Exception as e:
        return f"Error al obtener el enlace m3u8: {str(e)}"  # Return error message if an exception occurs

@app.get("/get_m3u8/")
def get_m3u8(url: str):
    driver = configurar_navegador()  # Configure the browser driver
    m3u8_url = obtener_m3u8_link(driver, url)  # Get the m3u8 URL from the provided URL
    driver.quit()  # Close the browser driver

    if m3u8_url:
        return {"m3u8_url": m3u8_url}  # Return the m3u8 URL if found
    else:
        return {"error": "No se encontró el enlace m3u8 en la página proporcionada."}  # Return an error message if not found

@app.get("/")
def read_root():
    return {"Hello": "Estás conectado"}  # Basic endpoint to confirm the API is running

# To run the app: uvicorn main:app --reload

# For Heroku deployment (these are terminal commands, not part of the Python code):
# heroku buildpacks:add https://github.com/heroku/heroku-buildpack-chrome-for-testing --app jkanami-api-v0


# ejecutar api
# uvicorn main:app --reload


#heroku buildpacks:add https://github.com/heroku/heroku-buildpack-chrome-for-testing --app jkanami-api-v0
