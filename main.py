import configparser
import time
import logging.config
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChService
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import contextlib

webdriver_config = configparser.ConfigParser()

# Read the config.ini file
webdriver_config.read("config/config.ini")

# Create a logger with a descriptive name
logger = logging.getLogger("EnebaScraper")

# Set the level of the logger to ERROR
logger.setLevel(logging.ERROR)

# Create a file handler with a file name and mode
fh = logging.FileHandler("logs\\error.log", mode="a")

# Create a formatter with a format string
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

# Add the formatter to the file handler
fh.setFormatter(formatter)

# Add the file handler to the logger
logger.addHandler(fh)

# Use a context manager to automatically close the file handler
with contextlib.closing(fh):
    class EnebaScraper:
        def __init__(self):
            self.driver_path = webdriver_config.get("WEBDRIVER", "driver_path")
            self.url = webdriver_config.get("WEBDRIVER", "url")
            self.min_price = webdriver_config.get("WEBDRIVER", "min_price")
            self.wait_time = webdriver_config.getint("WEBDRIVER", "wait_time")
            self.game_prices = []
            self.game_names = []
            self.game_card_regions = []
            self.wish_list_count = []

        def start(self):
            try:
                op = webdriver.ChromeOptions()
                with webdriver.Chrome(service=ChService(self.driver_path),
                                      options=op) as self.edriver:
                    self.edriver.get(self.url)
                    self.edriver.maximize_window()
                    self.accept_cookies()
                    self.set_min_price()
                    self.scrape_games()
                    self.save_data()
            except (Exception, ):
                # Add the file handler to the logger
                logger.error("Exception occurred in accept_cookies part", exc_info=True)

        def accept_cookies(self):
            try:
                select_all = '//*[@id="app"]/div/div/div[2]/div[2]/div/button[1]/span'
                wait = WebDriverWait(self.edriver, self.wait_time)
                accept_cookies = wait.until(EC.element_to_be_clickable((By.XPATH, select_all)))
                accept_cookies.click()
                time.sleep(4)
            except (Exception, ):
                # Add the file handler to the logger
                logger.error("Exception occurred in accept_cookies part", exc_info=True)

        def set_min_price(self):
            # this part is needed to get rid of sold out games, if you enter minimal value, then they disappear.
            try:
                min_price_input = ('#app > main > div > div.Gn2rwQ > aside > form > div.cE2dbi > div:nth-child(2) > '
                                   'div > input:nth-child(1)')
                wait = WebDriverWait(self.edriver, self.wait_time)
                wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, min_price_input)))
                input_element = self.edriver.find_element(By.CSS_SELECTOR, min_price_input)
                input_element.send_keys(self.min_price)
                time.sleep(3)
            except (Exception, ):

                # Add the file handler to the logger
                logger.error("Exception occurred in set_min_price part", exc_info=True)

        def scrape_games(self):
            while True:
                try:
                    # Scrolling down slowly for data to show up
                    time.sleep(3)
                    total_height = int(self.edriver.execute_script("return document.body.scrollHeight"))
                    for i in range(1, total_height, 5):
                        self.edriver.execute_script("window.scrollTo(0, {});".format(i))

                    # finding data by the class name and storing it
                    all_prices = self.edriver.find_elements(By.CLASS_NAME, 'L5ErLT')
                    prices = [price.text for price in all_prices]
                    self.game_prices.append(prices)
                    all_names = self.edriver.find_elements(By.CLASS_NAME, 'YLosEL')
                    names = [name.text for name in all_names]
                    self.game_names.append(names)
                    all_regions = self.edriver.find_elements(By.CLASS_NAME, 'Pm6lW1')
                    regions = [region.text for region in all_regions]
                    self.game_card_regions.append(regions)
                    wish_lists = self.edriver.find_elements(By.CLASS_NAME, 'BwtiXe')
                    wishes = [wish_list.text for wish_list in wish_lists]
                    self.wish_list_count.append(wishes)
                    # next page button
                    next_selector = 'rc-pagination-next'
                    press_next = self.edriver.find_element(By.CLASS_NAME, next_selector)
                    if 'rc-pagination-next rc-pagination-disabled' in press_next.get_attribute('class'):
                        print("No more pages to scrape")  # print a message to the user
                        return
                    press_next.click()
                except KeyboardInterrupt:
                    raise
                except (Exception, ):
                    logger.error("Exception occurred in scrape_game part", exc_info=True)

        def save_data(self):
            try:
                # Assuming you have the scraped data in lists of lists, such as:
                # You can create a list of headers for the csv file, such as:
                headers = ['Price', 'Name', 'Region', 'Wish List']

                # You can create a list of rows for the csv file, by zipping the data lists together, such as:
                rows = []

                for page in zip(self.game_names, self.game_prices, self.game_card_regions, self.wish_list_count):
                    for game in zip(*page):
                        rows.append(game)

                # You can write the headers and rows to a csv file, using the csv module, such as:
                with open('eneba_games.csv', 'w', newline='') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(headers)
                    writer.writerows(rows)
            except KeyboardInterrupt:
                raise
            except (Exception, ):
                logger.error("Exception occurred in scrape_game part", exc_info=True)

            self.edriver.close()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    scraper = EnebaScraper()
    scraper.start()
