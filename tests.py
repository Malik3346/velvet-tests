from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import unittest
import time

BASE_URL = "http://3.93.164.111:5000"
def get_driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.binary_location = "/usr/bin/google-chrome"
    service = Service('/usr/local/bin/chromedriver')
    return webdriver.Chrome(service=service, options=options)
class VelvetFashionTests(unittest.TestCase):

    def setUp(self):
        self.driver = get_driver()
        self.wait = WebDriverWait(self.driver, 10)

    def tearDown(self):
        self.driver.quit()

    def test_01_homepage_loads(self):
        self.driver.get(BASE_URL)
        self.assertNotEqual(self.driver.title, "")

    def test_02_homepage_has_navbar(self):
        self.driver.get(BASE_URL)
        navbar = self.driver.find_element(By.TAG_NAME, "nav")
        self.assertTrue(navbar.is_displayed())

    def test_03_homepage_has_content(self):
        self.driver.get(BASE_URL)
        body = self.driver.find_element(By.TAG_NAME, "body").text
        self.assertGreater(len(body), 100)

    def test_04_login_page_loads(self):
        self.driver.get(f"{BASE_URL}/login")
        self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        self.assertIn("login", self.driver.current_url.lower())

    def test_05_login_has_email_field(self):
        self.driver.get(f"{BASE_URL}/login")
        self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "input")))
        inputs = self.driver.find_elements(By.TAG_NAME, "input")
        types = [i.get_attribute("type") for i in inputs]
        self.assertIn("email", types)

    def test_06_login_has_password_field(self):
        self.driver.get(f"{BASE_URL}/login")
        self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "input")))
        inputs = self.driver.find_elements(By.TAG_NAME, "input")
        types = [i.get_attribute("type") for i in inputs]
        self.assertIn("password", types)

    def test_07_login_invalid_credentials(self):
        self.driver.get(f"{BASE_URL}/login")
        self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "input")))
        inputs = self.driver.find_elements(By.TAG_NAME, "input")
        for inp in inputs:
            if inp.get_attribute("type") == "email":
                inp.send_keys("fake@fake.com")
            if inp.get_attribute("type") == "password":
                inp.send_keys("wrongpass")
        btn = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        btn.click()
        time.sleep(2)
        self.assertNotIn("/dashboard", self.driver.current_url)

    def test_08_register_page_loads(self):
        self.driver.get(f"{BASE_URL}/register")
        self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        self.assertIn("register", self.driver.current_url.lower())

    def test_09_register_has_fields(self):
        self.driver.get(f"{BASE_URL}/register")
        self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "input")))
        inputs = self.driver.find_elements(By.TAG_NAME, "input")
        self.assertGreaterEqual(len(inputs), 3)

    def test_10_register_has_submit(self):
        self.driver.get(f"{BASE_URL}/register")
        self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "button")))
        btn = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        self.assertTrue(btn.is_displayed())

    def test_11_shop_page_loads(self):
        self.driver.get(f"{BASE_URL}/shop")
        self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        self.assertEqual(self.driver.current_url, f"{BASE_URL}/shop")

    def test_12_shop_has_content(self):
        self.driver.get(f"{BASE_URL}/shop")
        self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        body = self.driver.find_element(By.TAG_NAME, "body").text
        self.assertGreater(len(body), 50)

    def test_13_cart_page_loads(self):
        self.driver.get(BASE_URL + "/cart")
        self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        self.assertIsNotNone(self.driver.find_element(By.TAG_NAME, "body"))

    def test_14_wishlist_page_loads(self):
        self.driver.get(BASE_URL + "/wishlist")
        self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        self.assertIsNotNone(self.driver.find_element(By.TAG_NAME, "body"))

    def test_15_profile_redirects(self):
        self.driver.get(f"{BASE_URL}/profile")
        self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        body = self.driver.find_element(By.TAG_NAME, "body").text
        self.assertTrue(
            "login" in self.driver.current_url.lower() or
            "login" in body.lower() or
            "sign" in body.lower()
        )

    def test_16_orders_page_loads(self):
        self.driver.get(f"{BASE_URL}/orders")
        self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        self.assertIsNotNone(self.driver.find_element(By.TAG_NAME, "body"))

    def test_17_checkout_page_loads(self):
        self.driver.get(f"{BASE_URL}/checkout")
        self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        self.assertIsNotNone(self.driver.find_element(By.TAG_NAME, "body"))

    def test_18_navbar_has_login(self):
        self.driver.get(BASE_URL)
        self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "nav")))
        page = self.driver.page_source.lower()
        self.assertTrue("login" in page or "sign in" in page)

    def test_19_title_not_empty(self):
        self.driver.get(BASE_URL)
        self.assertNotEqual(self.driver.title.strip(), "")

    def test_20_login_has_register_link(self):
        self.driver.get(f"{BASE_URL}/login")
        self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        page = self.driver.page_source.lower()
        self.assertTrue("register" in page or "sign up" in page)

if __name__ == '__main__':
    unittest.main(verbosity=2)
