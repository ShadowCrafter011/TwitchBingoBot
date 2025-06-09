from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, ElementClickInterceptedException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver import Remote, ChromeOptions
from selenium.webdriver.common.by import By
from termcolor import colored
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
        self.last_vote = -1
        self.channels = os.getenv("BINGO_CHANNELS").replace(" ", "").split(",")
        self.handles: list[list[str, str]] = []

        for channel in self.channels:
            if not channel in self.bingos:
                self.bingos[channel.lower().capitalize()] = 0

    def run(self):
        for _ in range(int(self.restart_timer / self.delay)):
            for channel, handle in self.handles:
                self.driver.switch_to.window(handle)
                self.run_driver(channel)

    def run_driver(self, channel: str):
        channel = channel.lower().capitalize()
        sleep(self.delay / len(self.handles))

        self.switch_to_inner_iframe()

        try:
            card = []
            for number in self.driver.find_elements(By.XPATH, "//button[contains(@class,'card-cell')]"):
                if "card-cell--marked" in number.get_attribute("class").split():
                    card.append(1)
                else:
                    card.append(0)
        except (NoSuchElementException, StaleElementReferenceException):
            pass

        best_index, best_value = 0, 0

        if len(card) == 5*5:
            # Check bingo rows
            for x in range(5):
                val = sum(card[x * 5:x * 5 + 5])
                if val > best_value and val < 5:
                    best_value = val
                    best_index = card[x * 5:x * 5 + 5].index(0) + x * 5

            # Check bingo columns
            for x in range(5):
                first_zero = -1
                val = 0
                for y in range(5):
                    card_val = card[y * 5 + x]
                    val += card_val
                    if card_val == 0:
                        first_zero = y * 5 + x
                if val > best_value and val < 5:
                    best_value = val
                    best_index = first_zero

            # Check diagonals
            diagonals = [
                [0, 6, 12, 18, 24],
                [4, 8, 12, 16, 20]
            ]
            for diag in diagonals:
                val = 0
                first_zero = -1
                for index in diag:
                    card_val = card[index]
                    val += card_val
                    if card_val == 0:
                        first_zero = index
                if val > best_value and val < 5:
                    best_value = val
                    best_index = first_zero

        # Click on best bingo vote
        try:
            vote_number = self.driver.find_elements(By.XPATH, "//button[contains(@class,'card-cell')]")[best_index]
            if len(vote_number.find_elements(By.CLASS_NAME, "card-cell__bg.card-cell__bg--votable")) > 0 and self.last_vote != best_index:
                self.last_vote = best_index
                vote_number.click()
                print(f"Voted on ({channel}):")
                for x in range(len(card)):
                    if card[x] == 1:
                        print(colored(card[x], "green"), end=" ")
                    elif x == best_index:
                        print(colored(card[x], "red"), end=" ")
                    else:
                        print(card[x], end=" ")
                    if (x + 1) % 5 == 0:
                        print("")
        except (NoSuchElementException, StaleElementReferenceException, ElementClickInterceptedException, IndexError):
            pass                    
        
        # Join the bingo game
        try:
            join_button = self.driver.find_element(By.CLASS_NAME, "splash-screen__join-button")
            join_button.click()
        except (NoSuchElementException, StaleElementReferenceException, ElementClickInterceptedException):
            pass
        
        # Click on called cells
        try:
            for number in self.driver.find_elements(By.CLASS_NAME, "card-cell"):
                if len(number.find_elements(By.CLASS_NAME, "card-cell__bg.card-cell__bg--called")) > 0:
                    number.click()
                    sleep(.5)
        except (NoSuchElementException, StaleElementReferenceException, ElementClickInterceptedException):
            pass
        
        # Click the bingo button if bingo is reached
        try:
            win_button = self.driver.find_element(By.CLASS_NAME, "card-bingo-button.card-bingo-button__bingo-available")
            win_button.click()
            self.bingos[channel] += 1
            print(f"We got a BINGO! {self.bingos} gotten so far ({channel})")
        except (NoSuchElementException, StaleElementReferenceException, ElementClickInterceptedException):
            pass
        
        # DO NOT SPEND BITS AUTOMATICALLY
        try:
            self.driver.switch_to.default_content()
            cancel_bits_button = self.driver.find_element(By.XPATH, "//button[@data-test-selector='test_selector_cancel_button']")
            cancel_bits_button.click()
        except (NoSuchElementException, StaleElementReferenceException, ElementClickInterceptedException):
            pass

    def login(self):
        self.driver.get("https://twitch.tv")

        cookies = "DEBUG_TWITCH_COOKIES" if self.debug else "TWITCH_COOKIES"
        cookies = os.getenv(cookies).split(";")
        cookies = [cookie.strip().split("=") for cookie in cookies]
        
        for key, value in cookies:
            self.driver.add_cookie({"name": key, "value": value})

        for x, channel in enumerate(self.channels):
            url = f"BINGO_URL_{channel}"
            self.driver.get(os.getenv(url))
            self.driver.refresh()

            self.handles.append([
                channel,
                self.driver.current_window_handle
            ])

            if x < len(self.channels) - 1:
                self.driver.switch_to.new_window("tab")

    def switch_to_inner_iframe(self):
        iframe = self.driver.find_element(By.TAG_NAME, "iframe")
        self.driver.switch_to.frame(iframe)

        inner_iframe = self.driver.find_element(By.TAG_NAME, "iframe")
        self.driver.switch_to.frame(inner_iframe)

    def quit(self):
        self.driver.quit()
