import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

but = '//*[@id="app"]/main/div/div[2]/section/ul/li[7]/a'
op = webdriver.ChromeOptions()
game_prices = []
game_names = []
game_card_regions = []
wish_list_count = []
with webdriver.Chrome(service=ChService("Drivers/chromedriver.exe"),
                      options=op) as ffdriver:
    ffdriver.get("https://www.eneba.com/lt/store/mmo-games")
    ffdriver.maximize_window()
    select_all = '//*[@id="app"]/div/div/div[2]/div[2]/div/button[1]/span'
    wait = WebDriverWait(ffdriver, 15)
    accept_cookies = wait.until(EC.element_to_be_clickable((By.XPATH, select_all)))
    accept_cookies.click()
    time.sleep(4)
    min_price_input = '#app > main > div > div.Gn2rwQ > aside > form > div.cE2dbi > div:nth-child(2) > div > input:nth-child(1)'
    inputElement = ffdriver.find_element(By.CSS_SELECTOR, min_price_input)
    inputElement.send_keys('0.5')
    time.sleep(3)

    while True:
        try:

            time.sleep(3)
            total_height = int(ffdriver.execute_script("return document.body.scrollHeight"))
            for i in range(1, total_height, 5):
                ffdriver.execute_script("window.scrollTo(0, {});".format(i))
            # pr = '//*[@id="app"]/main/div/div[2]/section/div[2]/div[3]/div[1]/div/div[3]/a/div[1]/span[2]/span'
            # all_prices = ffdriver.find_elements(By.XPATH, pr)

            all_prices = ffdriver.find_elements(By.CLASS_NAME, 'L5ErLT')
            game_prices.append(all_prices)
            print([price.text for price in all_prices], len(all_prices))
            all_names = ffdriver.find_elements(By.CLASS_NAME, 'YLosEL')
            game_names.append(all_names)
            print([name.text for name in all_names], len(all_names))
            all_regions = ffdriver.find_elements(By.CLASS_NAME, 'Pm6lW1')
            game_card_regions.append(all_regions)
            print([region.text for region in all_regions], len(all_regions))
            wish_lists = ffdriver.find_elements(By.CLASS_NAME, 'BwtiXe')
            wish_list_count.append(wish_lists)
            print([wish_list.text for wish_list in wish_lists], len(wish_lists))
            # next_button = '// *[ @ id = "app"] / main / div / div[2] / section / ul / li[7] / a'
            next_selector = 'rc-pagination-next'
            press_next = ffdriver.find_element(By.CLASS_NAME, next_selector)
            if 'rc-pagination-next rc-pagination-disabled' in press_next.get_attribute('class'):
                break
            press_next.click()

        except Exception as e:
            print(e)
            break

    ffdriver.close()

# # Press the green button in the gutter to run the script.
# if __name__ == '__main__':
#     print('Hi')
#
# # See PyCharm help at https://www.jetbrains.com/help/pycharm/
