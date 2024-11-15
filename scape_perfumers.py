from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
import csv

chrome_options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=Service(
    ChromeDriverManager().install()), options=chrome_options)

url = "https://www.fragrantica.com/noses/"
driver.get(url)

time.sleep(3)
nose_elements = driver.find_elements(
    By.XPATH, '//div[@class="cell small-12 medium-4"]')
noses = []
for element in nose_elements:
    name_element = element.find_element(By.XPATH, './/a')
    perfumer_name = name_element.text
    perfumer_link = name_element.get_attribute('href')
    noses.append((perfumer_name, perfumer_link))

csv_filename = "noses.csv"
print(noses)
with open(csv_filename, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["Perfumer Name", "Perfumer Link"])
    writer.writerows(noses)

print(f"Data has been saved to {csv_filename}")
driver.quit()
