from bs4 import BeautifulSoup
# import requests
# import pandas as pd
from urllib.request import urlopen
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
import time
import undetected_chromedriver as uc


def scrape():
    links = []
    rev = []
    for no in range(1,3):
        url = f'https://alikaynaturals.com/collections/hair?page={no}&view=all'
        soup = BeautifulSoup(urlopen(url),'html.parser')
        items = soup.find_all('a',{"class":"product-title"})
        for item in items:
            links.append(item['href'])
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-notifications')
    options.add_argument('--no-sandbox')  # to bypass os security
    options.add_argument("--start-maximized") # setting the width for the browser
    # to overcome limited resources
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36")
    # service = Service(executable_path='/chromedriver/chromedriver-linux64/chromedriver')

    browser = uc.Chrome(options=options,detach=True,version_main=120)
    time.sleep(2)
    for link in links:
        browser.get(f'https://alikaynaturals.com{link}')
        time.sleep(2)
        product_name = browser.find_element(By.XPATH, ".//h1[@itemprop='name']").text.strip()
        description = browser.find_element(By.XPATH,'.//div[@id="tabs"]/div[1]').text.strip()
        ingredients = browser.find_element(By.XPATH,'.//div[@id="tabs"]/div[3]')
        ingredients = browser.execute_script("return arguments[0].textContent;", ingredients).strip()
    #     print('ingredients',ingredients)
        browser.find_element(By.ID,'ui-id-4').click()
        time.sleep(2)
        all_reviews = browser.find_elements(By.XPATH,'//div[@class="spr-review"]')
        page = 1
        for view in all_reviews:
            review_topic = view.find_element(By.XPATH,'.//div[@class="spr-review-header"]/h3').text.strip()
            review_author_data = view.find_element(By.XPATH,'.//div[@class="spr-review-header"]/span[2]').text.strip().split(' on ')
    #         review_author_data = browser.execute_script("return document.find(div[class=spr-review-header]  span:nth-child(3)).innerHTML")
            rating = view.find_element(By.XPATH,'.//span[@class="spr-starratings spr-review-header-starratings"]').get_attribute('aria-label')
            review_author = review_author_data[0]
            review_date = review_author_data[1]
            review_message = view.find_element(By.XPATH,'.//div[@class="spr-review-content"]').text.strip()
            data = {
                "product_name":product_name,
                "description": description,
                'ingredients': ingredients,
                'review topic': review_topic,
                'rating': rating,
                'author': review_author,
                'message': review_message,
                'date':review_date
            }
    #         print(data)
            rev.append(data)
        next_page = browser.find_elements(By.XPATH, './/span[@class="spr-pagination-next"]')
        if len(next_page) > 0:
            last_page = browser.find_element(By.XPATH,'(.//span[@class="spr-pagination-page"])[last()]').text.strip()
            while page < int(last_page):
                next_page[0].click()
                time.sleep(2)
                all_reviews = browser.find_elements(By.XPATH,'//div[@class="spr-review"]')
                for view in all_reviews:
                    review_topic = view.find_element(By.XPATH,'.//div[@class="spr-review-header"]/h3').text.strip()
                    review_author_data = view.find_element(By.XPATH,'.//div[@class="spr-review-header"]/span[2]').text.strip().split(' on ')
                    # print("author in the loop",review_author_data)
                    rating = view.find_element(By.XPATH,'.//span[@class="spr-starratings spr-review-header-starratings"]').get_attribute('aria-label')
                    review_author = review_author_data[0]
                    review_date = review_author_data[1]
                    review_message = view.find_element(By.XPATH,'.//div[@class="spr-review-content"]').text.strip()
                    next_page = browser.find_elements(By.XPATH, './/span[@class="spr-pagination-next"]')
                    data = {
                        "product_name":product_name,
                        "description": description,
                        'ingredients': ingredients,
                        'review topic': review_topic,
                        'rating': rating,
                        'author': review_author,
                        'message': review_message,
                        'date':review_date
                    }
                    rev.append(data)
                    # print("message in the javascript",review_message)
                page += 1
    browser.close()
    return rev

scrape()
# print(result)