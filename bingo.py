from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, ElementClickInterceptedException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver import Remote, ChromeOptions
from selenium.webdriver.common.by import By
from time import sleep
import os


class Bingo:
    def __init__(self, bingos, debug=False):
        options = ChromeOptions()
        options.add_argument("--window-size=400,1000")
        self.driver: Remote = Remote(os.getenv("SELENIUM_REMOTE_URL"), options=options)
        self.bingos = bingos
        self.delay = 5
        self.restart_timer = 10 * 60
        self.debug = debug

    def run(self):
        for _ in range(int(self.restart_timer / self.delay)):
            sleep(self.delay)

            self.switch_to_inner_iframe()

            try:
                join_button = self.driver.find_element(By.CLASS_NAME, "splash-screen__join-button")
                join_button.click()
            except (NoSuchElementException, StaleElementReferenceException, ElementClickInterceptedException):
                pass

            try:
                for number in self.driver.find_elements(By.CLASS_NAME, "card-cell"):
                    if len(number.find_elements(By.CLASS_NAME, "card-cell__bg.card-cell__bg--called")) > 0:
                        number.click()
                        sleep(.5)
            except (NoSuchElementException, StaleElementReferenceException, ElementClickInterceptedException):
                pass

            try:
                win_button = self.driver.find_element(By.CLASS_NAME, "card-bingo-button.card-bingo-button__bingo-available")
                win_button.click()
                self.bingos += 1
                print(f"We got a BINGO! {self.bingos} gotten so far")
            except (NoSuchElementException, StaleElementReferenceException, ElementClickInterceptedException):
                pass
            
            try:
                self.driver.switch_to.default_content()
                cancel_bits_button = self.driver.find_element(By.XPATH, "//button[@data-test-selector='test_selector_cancel_button']")
                cancel_bits_button.click()
            except (NoSuchElementException, StaleElementReferenceException, ElementClickInterceptedException):
                pass

    def login(self):
        self.driver.get("https://twitch.tv")

        if self.debug:
            cookies = "TWITCH_COOKIES_DEBUG"
            url = "BINGO_URL_DEBUG"
        else:
            cookies = "TWITCH_COOKIES"
            url = "BINGO_URL"

        cookies = os.getenv(cookies).split(";")
        cookies = [cookie.strip().split("=") for cookie in cookies]
        
        for key, value in cookies:
            self.driver.add_cookie({"name": key, "value": value})

        self.driver.get(os.getenv(url))
        self.driver.refresh()

    def switch_to_inner_iframe(self):
        iframe = self.driver.find_element(By.TAG_NAME, "iframe")
        self.driver.switch_to.frame(iframe)

        inner_iframe = self.driver.find_element(By.TAG_NAME, "iframe")
        self.driver.switch_to.frame(inner_iframe)


    def quit(self):
        self.driver.quit()
