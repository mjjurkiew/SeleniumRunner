from selenium.webdriver import Chrome
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, TimeoutException, \
    ElementClickInterceptedException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options

import json

class ElementNotFound(Exception):
    """"""


class SeleniumRunner():
    """"""
    def __init__(self):
        self.driver = Chrome(options=self.__load_options(), service=...)

    def __get_chromedriver_path(self) -> str:
        return json.load(open('config.json')).get('chromedriverPath')

    def __load_options(self) -> Options:
        options: Options = Options()
        config_options: dict = json.load(open('config.json')).get('chromeOptions')
        argument: str

        for argument in config_options.get(['add_argument']):
            options.add_argument(argument)

        for name, experimental_option in config_options.get(['add_experimental_option']):
            options.add_experimental_option(name, experimental_option)

        return options

    def wait_for_element_clickable(self, value: str, by: str = By.XPATH, timeout: int = 0) -> WebElement:
        try:
            return WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable((by, value)))
        except TimeoutException as e:
            raise ElementNotFound(f"Element {value} could not be found") from e

    def click_element(self, value: str, by: str = By.XPATH, timeout: int = 0) -> None:
        self.wait_for_element_clickable(value, by, timeout).click()
