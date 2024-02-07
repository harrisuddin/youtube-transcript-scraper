
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait

from time import sleep
import json

options = Options()
waittime = 30
# options.add_argument('--headless')
# options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

driver.get("https://www.youtube.com/watch?v=uILhdYr_UDs")

# Load cookies from the file
# with open("cookies.json", "r") as file:
#     cookies = json.load(file)
#     for cookie in cookies:
#         driver.add_cookie(cookie)
sleep(15)
# print(driver.title)
element = WebDriverWait(driver, waittime).until(EC.presence_of_element_located((By.ID, "description-inner")))
try:
  element.click()
  print("clicked here")
except:
  driver.execute_script("document.getElementById('description-inner').click();")
  print("clicked after error")

sleep(10.2)

transcript_selector = ".yt-spec-button-shape-next.yt-spec-button-shape-next--outline.yt-spec-button-shape-next--call-to-action.yt-spec-button-shape-next--size-m"

button_element = WebDriverWait(driver, waittime).until(EC.element_to_be_clickable((By.CSS_SELECTOR, transcript_selector)))

try:
  button_element.click()
except:
  print("transcript button click failed")

sleep(20)

# with open("cookies.json", "w") as file:
#     json.dump(driver.get_cookies(), file)

driver.close()