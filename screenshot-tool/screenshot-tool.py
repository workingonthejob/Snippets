from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import argparse
import sys

# Info on headless maximized windows
# https://stackoverflow.com/questions/45374377/not-able-to-maximize-chrome-window-in-headless-mode

DESCRIPTION = """
Takes repetitive screenshots of an element on a web page.
"""
X_DECK_CONTAINER = '//div[@class="deck-group"]'
X_NO_THANKS_BTN = '//button[@class="decline-button eu-cookie-compliance-default-button"]'
X_PLAYERS = './/h4'
X_HEADER = '//header'
TIMEOUT = 10


class ScreenshotTool():
    def __init__(self, url, output_dir, driver):
        self.output_dir = output_dir
        self.url = url
        self.driver = driver

    def run(self):
        self.driver.get(self.url)
        self.driver.execute_script(
            'document.querySelector("header").style.display = "none"')
        wait = WebDriverWait(self.driver, TIMEOUT)
        clickable = ec.element_to_be_clickable((By.XPATH, X_NO_THANKS_BTN))
        no_thanks_btn_elm = wait.until(clickable)
        no_thanks_btn_elm.click()
        decks = driver.find_elements(by=By.XPATH, value=X_DECK_CONTAINER)
        names = driver.find_elements(by=By.XPATH, value=X_PLAYERS)
        number_of_decks = len(decks)

        for i in range(number_of_decks):
            player_name = names[i].text.split(" ")[0]
            print("{}[{}/{}]".format(player_name, i + 1, number_of_decks))
            decks[i].location_once_scrolled_into_view
            decks[i].screenshot(r"{}\{}.png".format(self.output_dir, player_name))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=DESCRIPTION)
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(0)
    parser.add_argument("-d","--directory", help="The directory to save screenshots to.", default=r".\"")
    parser.add_argument("-u","--url", help="The page to start at or create screenshots of.", required=True)
    # Take no arguments. Only use it as a true/false flag. Using the flag will return a boolean of the actions.
    parser.add_argument("-t","--trigger", help="The directory to save screenshots to.", action='store_false')
    # For flags with dashed names the dashes are replaced with underscores so to call it use args.two_words
    parser.add_argument("-b","--two-words", help="The directory to save screenshots to.", action='store_false')
    args = parser.parse_args()

    # Define the options we want
    # More options here:
    # https://peter.sh/experiments/chromium-command-line-switches/
    options = Options()
    options.add_argument("--headless")
    # Starting maximized headless doesn't work correctly.
    options.add_argument("--window-size=1920x1080")
    driver = webdriver.Chrome(options=options)

    try:
        tool = ScreenshotTool(args.url, r"{}".format(args.directory), driver)
        tool.run()
    except Exception as e:
        print(e)
    except KeyboardInterrupt:
        pass
    finally:
        driver.quit()
