import time


from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementClickInterceptedException, \
    StaleElementReferenceException


class CareersPage:
    URL = "https://useinsider.com/careers/"
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)


    locations_block=(By.XPATH, "//*[@id ='career-our-location']//h3[contains(text(),'Our Locations')]")
    teams_block = (By.XPATH, "//a[contains(text(), 'See all teams')]")
    life_at_insider_block =(By.XPATH, "//h2[contains(text(), 'Life at Insider')]")
    qa_jobs_link = (By.XPATH, "//*[@id = 'page-head']/div/div/div[1]/div/div/a, 'See al QA jobs")

    def is_loaded(self):
        return self.driver.current_url.startswith(self.URL)


    def are_sections_visible(self):
        try:

            self.wait.until(EC.visibility_of_element_located(self.locations_block))


            self.wait.until(EC.visibility_of_element_located(self.teams_block))


            self.wait.until(EC.visibility_of_element_located(self.life_at_insider_block))

            return (
                    self.driver.find_element(*self.locations_block).is_displayed() and
                    self.driver.find_element(*self.teams_block).is_displayed() and
                    self.driver.find_element(*self.life_at_insider_block).is_displayed()
            )
        except (NoSuchElementException, TimeoutException) as e:
            print(f"Element is not seen or not loaded: {e}")
            return False



