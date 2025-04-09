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
        options.add_argument("--window-size=300,800")
        self.driver: Remote = Remote(os.getenv("SELENIUM_REMOTE_URL"), options=options)

    def run(self):
        while True:
            sleep(1)

            try:
                join_button = self.driver.find_element(By.CLASS_NAME, "splash-screen__join-button")
                join_button.click()
            except (NoSuchElementException, StaleElementReferenceException, ElementClickInterceptedException):
                pass

            try:
                for number in self.driver.find_elements(By.CLASS_NAME, "card-cell__number"):
                    number.click()
            except (NoSuchElementException, StaleElementReferenceException, ElementClickInterceptedException):
                pass

            try:
                win_button = self.driver.find_element(By.CLASS_NAME, "card-bingo-button")
                win_button.click()
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

        iframe = self.driver.find_element(By.TAG_NAME, "iframe")
        self.driver.switch_to.frame(iframe)

        inner_iframe = self.driver.find_element(By.TAG_NAME, "iframe")
        self.driver.switch_to.frame(inner_iframe)


    def quit(self):
        self.driver.quit()
