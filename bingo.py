from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, ElementClickInterceptedException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver import Remote, ChromeOptions
from selenium.webdriver.common.by import By
from time import sleep
import os


class Bingo:
    def __init__(self):
        options = ChromeOptions()
        options.add_argument("--window-size=400,1000")
        self.driver: Remote = Remote(os.getenv("SELENIUM_REMOTE_URL"), options=options)
        self.bingos = 0

    def run(self):
        while True:
            sleep(1)

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

        cookies = os.getenv("TWITCH_COOKIES").split(";")
        cookies = [cookie.strip().split("=") for cookie in cookies]
        
        for key, value in cookies:
            self.driver.add_cookie({"name": key, "value": value})

        self.driver.get(os.getenv("BINGO_URL"))
        self.driver.refresh()

    def switch_to_inner_iframe(self):
        iframe = self.driver.find_element(By.TAG_NAME, "iframe")
        self.driver.switch_to.frame(iframe)

        inner_iframe = self.driver.find_element(By.TAG_NAME, "iframe")
        self.driver.switch_to.frame(inner_iframe)


    def quit(self):
        self.driver.quit()
