import unittest
import time

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait


#from pages.qajobs_page2 import QAJobsPage
from pages.qajobs_page import QAJobsPage
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC


class MyTestCase(unittest.TestCase):

    def setUp(self):
        options = Options()
        options.add_argument("--incognito")
        self.driver = webdriver.Chrome(options=options)
        self.driver.maximize_window()
    def test_something(self):

        qa_page = QAJobsPage(self.driver)
        qa_page.open()
        qa_page.accept_cookies()
        qa_page.is_loaded()

        qa_page.click_see_all_jobs()
        qa_page.scroll_until_dropdowns_visible()
        qa_page.filter_jobs(location="Istanbul, Turkiye", department="Quality Assurance")

        time.sleep(3)

        # Check QA jobs list
        self.assertTrue(qa_page.jobs_list_visible(), "QA job list was not found")
        time.sleep(3)
        self.assertTrue(qa_page.jobs_list_visible(), "QA job list was not found")

        qa_page.reveal_and_click_first_view_role()
        WebDriverWait(self.driver, 10).until(EC.title_contains("Insider"))
        # Check whether lever page is opened or not
        self.assertIn("Insider", self.driver.title, "Lever Application Page was not opened")
        time.sleep(5)

    def tearDown(self):
        self.driver.quit()



if __name__ == '__main__':
    unittest.main()
