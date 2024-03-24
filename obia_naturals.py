"""
importing necessary libraries
"""
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import JavascriptException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotInteractableException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc
import time
import traceback
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
from urllib.request import urlopen

def scrape():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-notifications')
    options.add_argument('--no-sandbox')  # to bypass os security
    options.add_argument("--start-maximized") # setting the width for the browser
    # to overcome limited resources
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36")
    browser = uc.Chrome(options=options,detach=True)
    time.sleep(5)
    action = ActionChains(browser)
    wait = WebDriverWait(browser, 10)
    data_list = {}

    try:
        product_list = []
        url = "https://www.obianaturals.com/collections/all/"
        soup = BeautifulSoup(urlopen(url),'html.parser')
        products_links = soup.find_all('div',{"class":"grid-product__content"})
        links = [product.find('a') for product in products_links]
        [product_list.append(str(link).split('"')[3]) for link in links]
    except Exception as e:
        print(e)
    main_page = "https://www.obianaturals.com/"
    for product_link in product_list:
        final_data = []
        link = main_page + product_link
        print()
        browser.get(link)
        print(browser.current_url)
        product_name = browser.find_element(By.XPATH, '//div[@class="product-block product-block--header"]//h1').get_attribute("innerHTML").strip()
        print(f"getting data for {product_name}...")
        info = browser.find_element(By.XPATH, '//div[@class="rte"]').get_attribute("innerHTML")
        try:
            product_desc = info.split("Description</span>:</strong></p>")[1].split("</p>")[0]
            product_directions = info.split("Directions for Use</span>: </strong></p>")[1].split("</p>")[0]
            product_ingredients = info.split("Ingredients</span>:&nbsp;</strong><span>")[1].split("</p>")[0]
        except IndexError:
            try:
                pcroduct_desc = info.split("Description:</strong></span></p>")[1].split("</p>")[0]
            except IndexError:
                pcroduct_desc = info.split("Description:</strong> </span></p>")[1].split("</p>")[0]
                # try:
            try:
                product_directions = info.split("Directions for Use:</strong> </span></p>")[1].split("</p>")[0]
            except IndexError:
                product_directions = info.split("Directions for Use:</strong></span></p>")[1].split("</p>")[0]
            try:
                product_ingredients = info.split("Ingredients:</span>&nbsp;</strong>")[1].split("</p>")[0]
            except IndexError:
                product_ingredients = info.split("Ingredients:&nbsp;</strong></span>")[1].split("</p>")[0]
        except Exception:
            product_desc = ""

        product_data = {
                            "product_name": product_name,
                            "product_desc": product_desc,
                            "product_ingredients": product_ingredients,
                            "product_directions": product_directions
                        }
        
        reviews = browser.find_elements(By.XPATH, './/div[@class="spr-review"]')
        for review in reviews:
            data = {}
            review_topic = review.find_element(By.XPATH, './/h3[@class="spr-review-header-title"]').get_attribute('innerHTML')
            reviewer_name = review.find_element(By.XPATH, './/span[@class="spr-review-header-byline"]//strong').get_attribute('innerHTML')
            review_content = review.find_element(By.XPATH, './/p[@class="spr-review-content-body"]').get_attribute('innerHTML')
            review_date = review.find_elements(By.XPATH, './/span[@class="spr-review-header-byline"]//strong')[1].get_attribute('innerHTML')
            rating_count = review.find_elements(By.XPATH, './/div[@class="spr-review-header"]//i[@class="spr-icon spr-icon-star"]')
            review_rating = (len(rating_count))

            data["product_name"] = product_name,
            data["product_name"] = product_desc,
            data["product_name"] = product_ingredients,
            data["product_name"] = product_directions
            data["review_topic"] = review_topic
            data["reviewer_name"] = reviewer_name
            data["review_content"] = review_content
            data["review_date"] = review_date
            data["review_rating"] = review_rating
            print(data)
            final_data.append(data)
        data_list[product_name] = final_data
        
scrape()
