from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By

class BookingFiltration:
    def __init__(self, driver: WebDriver):
        self.driver = driver

    def aplly_star_rating(self, *star_values):
        for star_value in star_values:
            star_filtration_box = self.driver.find_element(By.CSS_SELECTOR, f'[data-filters-item="class:class={star_value}"]')
            star_filtration_box.click()
    
    def sort_price_lowest_first(self):
        element = self.driver.find_element(By.CSS_SELECTOR, '[data-testid="sorters-dropdown-trigger"]')
        element.click()

        lowest_price = self.driver.find_element(By.CSS_SELECTOR, '[aria-label="Price (lowest first)"]')
        lowest_price.click()