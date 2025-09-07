import unittest


from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from pages.home_page import HomePage
from pages.careers_page import CareersPage



class TestInsiders(unittest.TestCase):


    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()

    def test_insider_careers_flow(self):
        # Open home page and check if loaded
        home_page = HomePage(self.driver)
        home_page.load()
        self.assertTrue(home_page.is_loaded(), "Home page failed to load")
        home_page.accept_cookies()
        # Click "Company" -> "Careers"
        home_page.click_company_menu()
        home_page.click_careers_menu()
        careers_page = CareersPage(self.driver)
        self.assertTrue(careers_page.is_loaded(), "Careers page failed to load")
        # Check sections visibility
        self.assertTrue(careers_page.are_sections_visible(), "Careers sections are not visible")



    def tearDown(self):
        self.driver.quit()


if __name__ == '__main__':
    unittest.main()