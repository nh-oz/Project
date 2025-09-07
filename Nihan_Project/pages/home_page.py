
import selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class HomePage:
    URL = "https://useinsider.com/"

    def __init__(self, driver):
        self.driver = driver



    # Locators
    company_menu = (By.XPATH, "//nav//a[contains(text(), 'Company')]")
    careers_menu = (By.XPATH, "//nav//a[contains(text(), 'Careers')]")


    # Actions
    def load(self):
        self.driver.get(self.URL)

    def is_loaded(self):
        return self.driver.current_url == self.URL

    def accept_cookies(self):
        try:
            btn = WebDriverWait(self.driver, 3).until(
                EC.element_to_be_clickable((By.ID, "wt-cli-accept-all-btn"))
            )
            btn.click()
        except:
            pass


    def click_company_menu(self):
        self.driver.find_element(*self.company_menu).click()

    def click_careers_menu(self):
        self.driver.find_element(*self.careers_menu).click()


