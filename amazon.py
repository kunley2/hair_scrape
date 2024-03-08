from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import random

# Set up Chrome options
options = Options()
options.add_argument('--disable-gpu')  # Disable GPU hardware acceleration
options.add_argument('--disable-dev-shm-usage')  # Overcome limited resource problems
options.add_argument('--no-sandbox')  # Bypass OS security model, WARNING: NOT RECOMMENDED FOR PRODUCTION
options.add_argument("--start-maximized")  # Start maximized
options.add_argument('--disable-blink-features=AutomationControlled')  # Try to hide automation
options.add_argument('--lang=en-US')  # Set language to US English
options.add_experimental_option("excludeSwitches", ["enable-automation"])  # Avoid Chrome's automation extension
options.add_experimental_option('useAutomationExtension', False)

# User-agent update to match ChromeDriver version and seem more natural
user_agent = "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"
options.add_argument(user_agent)

# Launch Chrome
driver = webdriver.Chrome(options=options)
driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

# Navigate to Amazon with delays to mimic human behavior
url = 'https://www.amazon.com'
driver.get(url)
time.sleep(random.uniform(2, 4))  # Wait for a few seconds

# Additional Strategies

# Simulate human-like browsing patterns, e.g., scrolling
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
time.sleep(random.uniform(1, 3))  # Random wait time
driver.execute_script("window.scrollTo(0, 0);")
time.sleep(random.uniform(1, 3))

# After your operations, consider persisting cookies and using them in future sessions
# This step would involve saving cookies to a file and then loading them before navigating to Amazon

# IMPORTANT: Use explicit waits rather than fixed sleeps to wait for elements
# Example of explicit wait usage:

# After your tasks
# driver.quit()



def get_reviews(driver):
    translate_button = driver.find_elements(By.XPATH, '//*[contains(@id, "cr-translate")]')
    if translate_button:
        driver.execute_script("arguments[0].click();", translate_button[0])
    time.sleep(2)
    reviews = driver.find_elements(By.XPATH, '//*[contains(@id, "customer_review")]')

    review_comments = []
    review_names = []
    review_ratings = [] #".review-rating"
    review_dates = []
    review_images = []

    for index in range(len(reviews)):
        review = reviews[index]

        reviewer_name = review.find_element(By.XPATH, './/*[contains(@class, "profile-name")]')
        review_names.append(reviewer_name.text)

        reviewer_rating = review.find_element(By.XPATH, './/*[contains(@data-hook, "review-star-rating")]')
        review_ratings.append(reviewer_rating.get_attribute("innerHTML"))

        reviewer_comment = review.find_element(By.XPATH, './/*[contains(@class, "reviewText") or contains(@class, "review-text")]')
        review_comments.append(reviewer_comment.text)

        review_date = review.find_element(By.XPATH, './/*[contains(@class, "review-date")]')
        review_dates.append(review_date.text)

        review_images_checker = review.find_elements(By.XPATH, './/*[@class="review-image-tile-section"]')
        
        if review_images_checker:
            images = review.find_elements(By.XPATH, './/a//img[@alt="Customer image"]')
            image_list = []
            for i in images:
                # Scroll to each image
                driver.execute_script("arguments[0].scrollIntoView();", i)
                
                # Add a small delay to ensure the image is loaded after scrolling
                time.sleep(1)  # Adjust the sleep time as needed

                # Get the 'src' attribute and add it to the list
                image_src = i.get_attribute("src")
                if image_src:
                    image_list.append(image_src)
        else:
            image_list = []
        review_images.append(image_list)

        

            

    return review_names, review_ratings, review_comments, review_dates, review_images






def main_scraper(find_product):

    wait = WebDriverWait(driver, 3)
    first_page = wait.until(EC.element_to_be_clickable((By.TAG_NAME, "body")))
    time.sleep(10)

    all = driver.find_element(By.XPATH, '/html/body')
    print(all.text)
    main_search = driver.find_element(By.XPATH, '//input[contains(@placeholder,"Search ") and @type="text"]')
    main_search.send_keys(find_product)
    main_search.send_keys(Keys.ENTER)

    products_data = []

    scraping_products = True
    j=0

    while scraping_products:

        products = driver.find_elements(By.XPATH, f"//*[contains(@class,'puis-padding-right-small')]//*[contains(translate(text(),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'), '{find_product}')]/ancestor::div[@data-cy='title-recipe']//h2//a")
        #'//*[contains(@class,"puis-padding-right-small")]//*[contains(text(), "Mielle") or contains(text(), "MIELLE")]')#'//*[contains(@data-cy, "title-recipe")]//h2//a//span[contains(text(), "Mielle") or contains(text(), "MIELLE")]')

        print("PRODUCTS FOUND: ", len(products))

        for product_index in range(len(products)):

            # ActionChains(driver).key_down(Keys.COMMAND).click(products[product_index]).key_up(Keys.COMMAND).perform() 

            href = products[product_index].get_attribute('href')
            # open in new tab
            driver.execute_script("window.open('%s', '_blank')" % href)
            
            time.sleep(7)
            driver.switch_to.window(driver.window_handles[1])

            product_dict = {}

            el1 = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body")))

            product_names = []
            product_name = driver.find_element(By.CSS_SELECTOR, '#productTitle')
            product_names.append(product_name.text)

            print("PRODUCT NAME: ", product_names)

            brands = []
            brand = driver.find_elements(By.CSS_SELECTOR, '.po-brand .a-span9 .a-size-base')
            for i in brand:
                brands.append(i.text)

            ingredients = []
            ingredient = driver.find_elements(By.CSS_SELECTOR, 'div.a-section.content')
            for i in ingredient:
                ingredients.append(i.text)

            print("collecting reviews")

            review_comments_main = []
            review_names_main = []
            review_ratings_main = [] 
            review_dates_main = []
            review_images_main = []
            i=0
            scraping_reviews = True
            while scraping_reviews:

                review_names, review_ratings, review_comments, review_dates, review_images = get_reviews(driver)

                review_comments_main.extend(review_comments)
                review_names_main.extend(review_names)
                review_ratings_main.extend(review_ratings) 
                review_dates_main.extend(review_dates)
                review_images_main.extend(review_images)




                all_reviews_button = driver.find_elements(By.XPATH, '//*[contains(@data-hook, "reviews-link")]')
                next_button_reviews = driver.find_elements(By.XPATH, '//*[@class="a-last"]//a')
                i+=1
                if all_reviews_button and i==1:
                    driver.execute_script("arguments[0].scrollIntoView();",all_reviews_button[0])
                    time.sleep(1)
                    driver.execute_script("arguments[0].click();", all_reviews_button[0])
                    time.sleep(5)
                    print("ALL REVIEW BUTTON")

                elif next_button_reviews and i>1:
                    driver.execute_script("arguments[0].scrollIntoView();",next_button_reviews[0])
                    time.sleep(1)
                    driver.execute_script("arguments[0].click();", next_button_reviews[0])
                    time.sleep(5)
                    print("NEXT BUTTON REVIEWS")

                else:
                    scraping_reviews = False

                
                # if i==3:
                #     scraping_reviews=False

                time.sleep(15)


            product_dict['product_name'] = product_names
            product_dict['product_brand'] = brands
            product_dict['product_ingredients'] = ingredients
            product_dict['review_ratings'] = review_ratings_main
            product_dict['reviewer_name'] = review_names_main
            product_dict['reviewer_comment'] = review_comments_main
            product_dict['review_date'] = review_dates_main
            product_dict['review_images'] = review_images_main

            products_data.append(product_dict)
            
            # //*[contains(@data-hook, "see-all-reviews")]
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            # if product_index==3:
            #     break


        

        j+=1
        next_button_products = driver.find_elements(By.XPATH, '//a[contains(@class, "s-pagination-next")]')

        if next_button_products:
            driver.execute_script("arguments[0].click();", next_button_products[0])
            time.sleep(15)
            print(f"NEXT BUTTON PRODUCTS. GOING TO PAGE: {j+1}")
            print("j:", j)

        else:
            scraping_products = False

    return products_data




find_product = ['camille rose', 'TGIN', 'alikay', 'as i am', 'curls', 'eden bodyworks', 'taliah']

data = []

for i in find_product:
    data_scraped = main_scraper(i)
    data.extend(data_scraped)


import pandas as pd
import datetime

date = datetime.datetime.now()

df = pd.DataFrame(data)
df.to_csv(f'amazon_com_data_{date}_3.csv', index=False)