import time
import logging
import logging.config
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChService
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv

logging.basicConfig(
  filename='main.log',
  level=logging.INFO,
  format='%(asctime)s :: %(levelname)s : %(name)s : %(message)s : line: %(lineno)d'
)


class EnebaScraper:
    def __init__(self, driver_path, url):
        self.driver_path = driver_path
        self.url = url
        self.game_prices = []
        self.game_names = []
        self.game_card_regions = []
        self.wish_list_count = []

    def start(self):
        op = webdriver.ChromeOptions()
        with webdriver.Chrome(service=ChService(self.driver_path),
                              options=op) as self.edriviver:
            self.edriviver.get(self.url)
            self.edriviver.maximize_window()
            self.accept_cookies()
            self.set_min_price('0.5')
            self.scrape_games()

    def accept_cookies(self):
        select_all = '//*[@id="app"]/div/div/div[2]/div[2]/div/button[1]/span'
        wait = WebDriverWait(self.edriviver, 15)
        accept_cookies = wait.until(EC.element_to_be_clickable((By.XPATH, select_all)))
        accept_cookies.click()
        time.sleep(4)

    def set_min_price(self, value):
        min_price_input = '#app > main > div > div.Gn2rwQ > aside > form > div.cE2dbi > div:nth-child(2) > div > input:nth-child(1)'
        wait = WebDriverWait(self.edriviver, 15)
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, min_price_input)))
        inputElement = self.edriviver.find_element(By.CSS_SELECTOR, min_price_input)
        inputElement.send_keys(value)
        time.sleep(3)

    def scrape_games(self):
        while True:
            try:
                # Scrolling down slowly for data to show up
                time.sleep(3)
                total_height = int(self.edriviver.execute_script("return document.body.scrollHeight"))
                for i in range(1, total_height, 5):
                    self.edriviver.execute_script("window.scrollTo(0, {});".format(i))
                # pr = '//*[@id="app"]/main/div/div[2]/section/div[2]/div[3]/div[1]/div/div[3]/a/div[1]/span[2]/span'
                # all_prices = edriviver.find_elements(By.XPATH, pr)

                all_prices = self.edriviver.find_elements(By.CLASS_NAME, 'L5ErLT')
                self.game_prices.append(all_prices)
                all_names = self.edriviver.find_elements(By.CLASS_NAME, 'YLosEL')
                self.game_names.append(all_names)
                all_regions = self.edriviver.find_elements(By.CLASS_NAME, 'Pm6lW1')
                self.game_card_regions.append(all_regions)
                wish_lists = self.edriviver.find_elements(By.CLASS_NAME, 'BwtiXe')
                self.wish_list_count.append(wish_lists)
                # next page button
                next_selector = 'rc-pagination-next'
                press_next = self.edriviver.find_element(By.CLASS_NAME, next_selector)
                if 'rc-pagination-next rc-pagination-disabled' in press_next.get_attribute('class'):
                    break
                press_next.click()

            except Exception as e:
                logging.error("Exception occurred", exc_info=True)
                print(e)
                break

        def save_data(self):
            # Assuming you have the scraped data in lists of lists, such as:
            # game_prices = [['0.99', '1.49', '2.99'], ['3.99', '4.99', '5.99']]
            # game_names = [['World of Warcraft', 'Final Fantasy XIV', 'Guild Wars 2'], ['EVE Online', 'Star Wars: The Old Republic', 'The Elder Scrolls Online']]
            # game_card_regions = [['Europe', 'Global', 'Europe'], ['Global', 'Global', 'Europe']]
            # wish_list_count = [['12', '34', '56'], ['78', '90', '12']]

            # You can create a list of headers for the csv file, such as:
            headers = ['Price', 'Name', 'Region', 'Wish List']

            # You can create a list of rows for the csv file, by zipping the data lists together, such as:
            rows = []
            for page in zip(self.game_prices, self.game_names, self.game_card_regions, self.wish_list_count):
                for game in zip(*page):
                    rows.append(game)

            # You can write the headers and rows to a csv file, using the csv module, such as:
            with open('eneba_games.csv', 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(headers)
                writer.writerows(rows)

        self.edriviver.close()



##### Loging part
# Import the logging module
# import logging
#
# # Create a logger object with the name of your choice
# logger = logging.getLogger("my_logger")
#
# # Set the level of the logger to DEBUG or higher
# logger.setLevel(logging.DEBUG)
#
# # Create a file handler object to write the logs to a file
# file_handler = logging.FileHandler("logs/error.log")
#
# # Set the level of the file handler to ERROR or higher
# file_handler.setLevel(logging.ERROR)
#
# # Create a formatter object to format the log messages
# formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
#
# # Set the formatter for the file handler
# file_handler.setFormatter(formatter)
#
# # Add the file handler to the logger
# logger.addHandler(file_handler)
#
# # Use the logger object to log messages with different levels
# logger.debug("This is a debug message")
# logger.info("This is an info message")
# logger.warning("This is a warning message")
# logger.error("This is an error message")
# logger.critical("This is a critical message")
#
# # You can also use the logger to log exceptions with traceback
# try:
#     x = 1 / 0
# except ZeroDivisionError:
#     logger.exception("This is an exception message")

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    scraper = EnebaScraper("Drivers/chromedriver.exe", "https://www.eneba.com/lt/store/mmo-games")
    scraper.start()
    print('Hi')



logging.info('{} : {}'.format('Addition result', ...))
