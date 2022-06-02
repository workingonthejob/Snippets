from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import argparse
import sys
import time

# Info on headless maximized windows
# https://stackoverflow.com/questions/45374377/not-able-to-maximize-chrome-window-in-headless-mode

X_NO_THANKS_BTN = '//button[@class="decline-button eu-cookie-compliance-default-button"]'
X_PLAYERS = './/h4'
X_HEADER = '//header'


class ScreenshotTool():
    def __init__(self, url, output_dir):
        self.output_dir = output_dir
        self.url = url

    def run(self):
        driver.get(self.url)
        time.sleep(2)
        driver.execute_script('document.querySelector("header").style.display = "none"')
        no_thanks_btn_elm = driver.find_element(by=By.XPATH, value=X_NO_THANKS_BTN)
        no_thanks_btn_elm.click()
        time.sleep(2)
        decks = driver.find_elements(by=By.XPATH, value='//div[@class="deck-group"]')
        names = driver.find_elements(by=By.XPATH, value=X_PLAYERS)
        number_of_decks = len(decks)

        for i in range(number_of_decks):
            player_name = names[i].text.split(" ")[0]
            print("{}[{}/{}]".format(player_name, i + 1, number_of_decks))
            decks[i].location_once_scrolled_into_view
            time.sleep(1)
            decks[i].screenshot(r"{}\{}.png".format(self.output_dir, player_name))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(0)
    parser.add_argument("-d","--directory", help="The directory to save screenshots to.", default=r".\"")
    parser.add_argument("-u","--url", help="The page to start at or screenshot.", required=True)
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
        tool = ScreenshotTool(args.url, r"{}".format(args.directory))
        tool.run()
    except Exception as e:
        print(e)
    except KeyboardInterrupt:
        pass
    finally:
        driver.quit()
