from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import sys
import time


# from selenium.webdriver.common.action_chains import ActionChains
# actions = ActionChains(driver)
# actions.move_to_element(deck).perform()

X_NO_THANKS_BTN = '//button[@class="decline-button eu-cookie-compliance-default-button"]'
X_PLAYER = './/h4'

options = Options()

#options.headless = True
options.add_argument("--start-maximized")

driver = webdriver.Chrome(options=options)


try:
    driver.get('http://magic.wizards.com/en/articles/archive/mtgo-standings/modern-league-2022-05-27')
    time.sleep(5)
    elm = driver.find_element(by=By.XPATH, value=X_NO_THANKS_BTN)
    elm.click()
    time.sleep(5)
    decks = driver.find_elements(by=By.XPATH, value='//div[@class="deck-group"]')
    names = driver.find_elements(by=By.XPATH, value=X_PLAYER)

    for i in range(len(decks)):
        player_name = names[i].text.split(" ")[0]
        print("{}[{}]".format(player_name, i))
        decks[i].location_once_scrolled_into_view
        time.sleep(1)
        decks[i].screenshot("{}.png".format(player_name))

    #print(dir(elm))
    #print(dir(driver))
except Exception as e:
    print(e)
finally:
    driver.close()
