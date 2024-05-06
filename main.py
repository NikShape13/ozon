import time
import undetected_chromedriver
from bs4 import BeautifulSoup as BS
from constant import TOTAL_PAGES, BRAND_URL
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

chrome_options = Options()
chrome_options.add_argument("--headless")


def get_page_html(driver, url, max_retries=3):
    retries = 0
    while retries < max_retries:
        try:
            driver.get(url)
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "ix2")))
            return driver.page_source
        except Exception as e:
            print(f"Error getting page: {e}")
            retries += 1
            time.sleep(2)
    return None


with undetected_chromedriver.Chrome(options=chrome_options) as driver:
    for i in range(1, TOTAL_PAGES+1):
        page_url = f'{BRAND_URL}{i}'
        html = get_page_html(driver, page_url)
        if html is None:
            print(f"Failed to retrieve page {i}. Skipping...")
            continue

        soup = BS(html, 'html.parser')
        products = [x.find('a') for x in soup.find_all('div', class_='ix2')]

        for product in products:
            with open('links.txt', 'a') as file:
                file.write(
                    f"https://www.ozon.ru{product.get('href').split('?')[0]}\n")

        print(f'Parsed page {i}, appended links in links.txt')
