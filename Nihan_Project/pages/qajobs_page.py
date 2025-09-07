import time
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException, StaleElementReferenceException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



class QAJobsPage:
    URL = "https://useinsider.com/careers/quality-assurance/"

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    # --- Locators ---
    see_all_qa_jobs = (By.XPATH, "//a[contains(., 'See all QA jobs')]")
    location_dropdown = (By.XPATH, "//*[@id='select2-filter-by-location-container']")
    department_dropdown = (By.XPATH, "//*[@id='select2-filter-by-department-container']")

    # Açılır listeye (dropdown) tıkladığımızda, gerçekten açıldığını doğrulamak istedim.
    # Bu görünür değilse seçenekler seçilemez.
    SELECT2_OPEN_CONTAINER = (By.CSS_SELECTOR, ".select2-container--open")

    # Dropdown açıldığında seçenekleri gösteren panel.

    RESULTS_PANEL = (By.CSS_SELECTOR, "ul.select2-results__options, .select2-results")

    # Kaç seçeneğin yüklendiğini saymak için kullanıldı.
    # Örneğin yalnızca "All" seçeneği varsa, liste henüz yüklenmemiş demektir;
    # 10'dan fazla seçenek görünüyorsa, hazırdır.
    OPTION_ITEMS = (By.CSS_SELECTOR, "li.select2-results__option[role='option']")

    # Filtre uygulandıktan sonra iş ilanlarının gerçekten listelendiğini doğrular.
    JOB_LIST_ITEMS = (By.CSS_SELECTOR, "div.position-list-item, .jobs-list .job, [data-position-id]")

    #  Basit sayfa kontrolleri
    def open(self):
        self.driver.get(self.URL)

    def is_loaded(self):
        return self.driver.current_url.startswith(self.URL)

    def accept_cookies(self):
        try:
            btn = WebDriverWait(self.driver, 3).until(
                EC.element_to_be_clickable((By.ID, "wt-cli-accept-all-btn"))
            )
            btn.click()
        except Exception:
            pass

    #  Yardımcılar
    def option_with_text(self, text):
        """Tam eşleşmeli option locatörü."""
        return (By.XPATH, f"//li[@role='option' and normalize-space()='{text}']")



    def _safe_click(self, el):
        try:
            el.click()
        except Exception:
            self.driver.execute_script("arguments[0].click();", el)



    def _open_select2_and_wait(self, trigger_locator, timeout=2):
        """Dropdown tetikleyicisini aç ve kısa bekle."""
        we = self.wait.until(EC.element_to_be_clickable(trigger_locator))
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", we)

        for method in ("click", "js", "ac"):
            try:
                if method == "click":
                    we.click()
                elif method == "js":
                    self.driver.execute_script("arguments[0].click();", we)
                else:
                    ActionChains(self.driver).move_to_element(we).pause(0.05).click().perform()

                WebDriverWait(self.driver, timeout).until(
                    EC.presence_of_element_located(self.SELECT2_OPEN_CONTAINER)
                )
                WebDriverWait(self.driver, timeout).until(
                    EC.presence_of_element_located(self.RESULTS_PANEL)
                )
                return
            except Exception:
                pass
        raise TimeoutException("Select2 dropdown could not be opened.")

    def _wait_some_options(self, min_options=3, timeout=3, poll=0.1):
        """Panel açıkken, yeterli sayıda seçenek yüklenene kadar bekle (kısaltılmış)."""
        end = time.time() + timeout
        while time.time() < end:
            if len(self.driver.find_elements(*self.OPTION_ITEMS)) >= min_options:
                return True
            time.sleep(poll)
        return False

    def _click_option_clickable(self, locator, timeout=1):
        el = WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable(locator))
        self._safe_click(el)

    def _close_select2(self, timeout=2):
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.invisibility_of_element_located(self.SELECT2_OPEN_CONTAINER)
            )
        except TimeoutException:
            pass

    def _wait_page_settle(self, seconds=1):
        """Kısa, bekleme gerektiğinde kullan."""
        start = time.time()
        WebDriverWait(self.driver, seconds).until(lambda d: time.time() - start >= seconds)

    # Akış
    def click_see_all_jobs(self, timeout=12, step_px=250, pause=0.2):
        self.driver.execute_script("window.scrollTo(0, 0);")
        end_time = time.time() + timeout
        while time.time() < end_time:
            try:
                btn = self.driver.find_element(*self.see_all_qa_jobs)
                if btn.is_displayed():
                    self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", btn)
                    time.sleep(0.05)
                    self._safe_click(btn)
                    time.sleep(0.2)
                    return
            except Exception:
                pass
            self.driver.execute_script(f"window.scrollBy(0,{step_px});")
            time.sleep(pause)
        raise TimeoutException("'See all jobs' button not found or clickable.")

    def scroll_until_dropdowns_visible(self, timeout=12):
        self._scroll_until_visible(self.location_dropdown, timeout=timeout)
        self._scroll_until_visible(self.department_dropdown, timeout=timeout)

    def _scroll_until_visible(self, locator, timeout=12, step_px=300, pause=0.2):
        end = time.time() + timeout
        while time.time() < end:
            try:
                el = self.driver.find_element(*locator)
                if el.is_displayed():
                    self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", el)
                    time.sleep(0.05)
                    return el
            except Exception:
                pass
            self.driver.execute_script(f"window.scrollBy(0,{step_px});")
            time.sleep(pause)
        raise TimeoutException(f"Element not visible: {locator}")

    def filter_jobs(self, location, department):
        """
        Sadece TAM EŞLEŞME ile seçim yapar.
        Akış:
          - LOCATION: Aç -- kısa liste bekle -- parametreyi seç.
                      Olmazsa: kapat -- biraz bekle -- tekrar aç --yine exact seç.
          - DEPARTMENT: Aynı şekilde sadece exact seç.
        """
        # --- LOCATION ---
        self._open_select2_and_wait(self.location_dropdown, timeout=3)
        self._wait_some_options(min_options=3, timeout=4)

        try:
            # parametreyle birebir eşleşen option
            self._click_option_clickable(self.option_with_text(location), timeout=2)
        except TimeoutException:
            # 1 kez kapat -- biraz bekle --tekrar aç -- tekrar dene
            try:
                from selenium.webdriver.common.keys import Keys
                from selenium.webdriver import ActionChains
                ActionChains(self.driver).send_keys(Keys.ESCAPE).perform()
                WebDriverWait(self.driver, 0.8).until(
                    EC.invisibility_of_element_located(self.SELECT2_OPEN_CONTAINER)
                )
            except Exception:
                try:
                    trig = self.driver.find_element(*self.location_dropdown)
                    self.driver.execute_script("arguments[0].click();", trig)  # toggle close
                    WebDriverWait(self.driver, 1.0).until(
                        EC.invisibility_of_element_located(self.SELECT2_OPEN_CONTAINER)
                    )
                except Exception:
                    pass

            self._wait_page_settle(2)#dropdown açılıp bekleme yapıp kapandıktan sonra 2 saniye kadar
            # tekrar dropdown unun açılmasını bekler.

            self._open_select2_and_wait(self.location_dropdown, timeout=3)
            self._wait_some_options(min_options=3, timeout=3, poll=0.12)
            # ikinci ve son exact deneme
            self._click_option_clickable(self.option_with_text(location), timeout=3)

        self._close_select2(timeout=2)

        # --- DEPARTMENT ---
        self._open_select2_and_wait(self.department_dropdown, timeout=3)
        self._wait_some_options(min_options=2, timeout=4)

        # yalnızca parametreyle birebir eşleşen option
        self._click_option_clickable(self.option_with_text(department), timeout=2)

        self._close_select2(timeout=2)
        time.sleep(0.2)  # görsel güncelleme için kısa bekleme


    def jobs_list_visible(self):
        """İlanlar geliyor mu ve metin kriterlerini sağlıyor mu?"""
        try:
            items = self.wait.until(EC.presence_of_all_elements_located(self.JOB_LIST_ITEMS))
            if not items:
                return False

            for job in items:
                self.driver.execute_script("window.scrollBy(0, 200);")
                txt = job.text
                if ("Quality Assurance" not in txt) or not (
                    "Istanbul, Turkiye" in txt or "Istanbul, Turkey" in txt
                ):
                    return False
            return True
        except TimeoutException:
            return False

    def reveal_and_click_first_view_role(self, pause=0.15, max_retries=3):
        """İlk kartı görünür yap -- hover --'View Role' tıkla; overlay/stale durumlarında tekrar dene."""
        card_locator = (By.XPATH, '//*[@id="jobs-list"]/div[1]/div')
        btn_rel_xpath = ".//a[contains(translate(normalize-space(.), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'view role')]"

        for attempt in range(1, max_retries + 1):
            try:
                card = self.wait.until(EC.visibility_of_element_located(card_locator))
                self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", card)
                self.driver.execute_script("window.scrollBy(0, 120);")
                time.sleep(pause)

                ActionChains(self.driver).move_to_element(card).pause(0.1).perform()
                time.sleep(pause)

                card = self.driver.find_element(*card_locator)  # hover sonrası tazele
                btn = card.find_element(By.XPATH, btn_rel_xpath)
                self.wait.until(EC.element_to_be_clickable(btn))

                try:
                    btn.click()
                except (ElementClickInterceptedException, StaleElementReferenceException):
                    self.driver.execute_script("arguments[0].click();", btn)
                return True

            except StaleElementReferenceException:
                if attempt == max_retries:
                    raise
                time.sleep(0.2)
            except TimeoutException:
                if attempt == max_retries:
                    raise
                time.sleep(0.2)
        return False

    def quit(self):
        if self.driver:
            try:
                self.driver.quit()
            except Exception as e:
                print(f"while closing Driver, there is an error: {e}")
