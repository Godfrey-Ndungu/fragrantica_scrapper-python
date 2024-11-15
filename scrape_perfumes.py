import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

chrome_options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=Service(
    ChromeDriverManager().install()), options=chrome_options)

csv_filename = "noses.csv"
perfumer_data = []

with open(csv_filename, mode='r', newline='', encoding='utf-8') as file:
    reader = csv.reader(file)
    next(reader)
    for row in reader:
        perfumer_name, perfumer_link = row
        perfumer_data.append((perfumer_name, perfumer_link))

output_filename = "perfumes.csv"

with open(output_filename, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=['Perfumer Name',
                                              'Perfume Name',
                                              'Perfume Link',
                                              'Type',
                                              'Year'])
    writer.writeheader()

    for perfumer_name, perfumer_link in perfumer_data:
        driver.get(perfumer_link)

        try:
            perfume_elements = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located(
                    (By.XPATH, '//div[contains(@class, "prefumeHbox")]'))
            )

            for element in perfume_elements:
                # Get perfume name, link, type, and year
                perfume_name_element = element.find_element(
                    By.XPATH, './/h3/a')
                perfume_name = perfume_name_element.text
                perfume_link = perfume_name_element.get_attribute('href')
                details = element.find_elements(
                    By.XPATH, './/div[contains(@class, "flex-container")]/span') # noqa
                perfume_type = details[0].text if len(details) > 0 else "N/A"
                perfume_year = details[1].text if len(details) > 1 else "N/A"

                writer.writerow({
                    'Perfumer Name': perfumer_name,
                    'Perfume Name': perfume_name,
                    'Perfume Link': perfume_link,
                    'Type': perfume_type,
                    'Year': perfume_year
                })
        except Exception as e:
            print(f"Error processing {perfumer_name} at {perfumer_link}: {e}")

# Clean up: Close the driver
driver.quit()

print(f"Data has been written to {output_filename}")
