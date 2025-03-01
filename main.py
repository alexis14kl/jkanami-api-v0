from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

# Set up Chrome options for headless mode
chrome_options = Options()
chrome_options.add_argument("--headless")  # Ensure chrome runs in headless mode
chrome_options.add_argument("--no-sandbox")  # Necessary for some environments like Heroku
chrome_options.add_argument("--disable-dev-shm-usage")  # Disable shared memory
chrome_options.add_argument("--disable-gpu")  # Disable GPU usage (not needed in headless mode)

# Create the WebDriver object
driver = webdriver.Chrome(options=chrome_options)

driver.get("https://www.selenium.dev/selenium/web/web-form.html")

title = driver.title

driver.implicitly_wait(0.5)

text_box = driver.find_element(by=By.NAME, value="my-text")
submit_button = driver.find_element(by=By.CSS_SELECTOR, value="button")

text_box.send_keys("Selenium")
submit_button.click()

message = driver.find_element(by=By.ID, value="message")
text = message.text

print(text)  # For debugging purposes

driver.quit()
