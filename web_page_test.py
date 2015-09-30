import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import testtools
import time

class WebpageTest(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome(executable_path = "C:\\Python34\\Scripts\\chromedriver.exe") # opens driver with Chrome browser
        self.base_url = "https://www.studentska-prehrana.si/Pages/Directory.aspx" # webpage url

    def test_word_in_title_in_webpage(self):
        """ Checks if webpage title contains the word "Imenik". """
        
        driver = self.driver
        driver.get(self.base_url)
        self.assertIn("Imenik", driver.title)
        
    def test_search_in_webpage(self):
        """ Checks if search engine doesn't return empty webpage for the word "Ljubljana". """
        
        driver = self.driver
        driver.get(self.base_url)
        elem = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "searchLocation"))) # wait until the search engine is not visible or 10 seconds
        elem.send_keys("Ljubljana") # enter word "Ljubljana"
        elem.send_keys(Keys.RETURN) # press RETURN button
        restaurants = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.TAG_NAME, "h2")))
        count = 0 # how many elements are visible
        for i in range(len(restaurants)):
            if restaurants[i].is_displayed():
                count += 1
        self.assertTrue(count > 0)

    def test_prices_in_webpage(self):
        """ Checks if the biggest price is lower than 10 EUR. """
        
        driver = self.driver
        driver.get(self.base_url)
        prices_found = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.TAG_NAME, "strong"))) # list
        prices = [] # list of discount prices
        for i in range(0, len(prices_found), 2): # every second price is discount
            number = prices_found[i].text # convert elements to string
            prices.append(float(number[:-7] + "." + number[-6:-4]))
        self.assertTrue(max(prices) < 10)

    def test_links_in_webpasge(self):
        """ Checks if hyperlink is working. """
        
        driver = self.driver
        driver.get(self.base_url)
        elem = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, "Novice"))) # wait until the link "Novice" is not clickable or 10 seconds
        elem.click()
        assert "trenutno niste prijavljeni." in driver.page_source

    def test_checkbox_in_webpage(self):
        """ Checks how many choices do we get if we select "dostava" and "študentske ugodnosti". """
        driver = self.driver
        driver.get(self.base_url)
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "rService5"))).click() # select "dostava"
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "rService9"))).click() # select "študentske ugodnosti"
        restaurants = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.TAG_NAME, "h2")))
        count = 0
        for i in range(len(restaurants)):
            if restaurants[i].is_displayed():
                count += 1
        self.assertEqual(count, 12) # check if list contains 12 elements
        
    def tearDown(self):
        self.driver.quit()

class TracingStreamResult(testtools.StreamResult):
    
    def status(self, *args, **kwargs):
        """ Function for printing results. """
        
        print('{0[test_id]}: {0[test_status]}'.format(kwargs))

if __name__ == "__main__":
    start = time.time()
    suite = unittest.TestLoader().loadTestsFromTestCase(WebpageTest)
    concurrent_suite = testtools.ConcurrentStreamTestSuite(lambda: ((case, None) for case in suite)) # performs all tests at the same time
    result = TracingStreamResult() # printing results
    result.startTestRun()
    concurrent_suite.run(result) # we run all tests at the same time
    result.stopTestRun()
    end = time.time()
    print(75*"-")
    print("Ran 5 tests in", round(end - start, 3), "s.")
