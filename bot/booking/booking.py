#Selenium Library's
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#Booking Objects and others
from booking.booking_filtration import BookingFiltration
from booking.booking_report import BookingReport
import booking.constants as const

#Others Library's and imports
from prettytable import PrettyTable
from types import TracebackType
from typing import Type
import time as time
import os

class Booking(webdriver.Firefox):
    def __init__(self, driver_path=r"C:/SeleniumDrivers", teardown=False):
        self.driver_path = driver_path
        self.teardown = teardown
        os.environ['PATH'] += self.driver_path
        super(Booking, self).__init__()
        self.implicitly_wait(3)
        self.maximize_window()
    
    #This function load the first page of the site Booking.com and close de pop-up
    #what spawn in the start of site
    def land_first_page(self):
        self.get(const.BASE_URL)
        wait = WebDriverWait(self, timeout=0.1)

        try:
            sing_in_element = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[aria-label="Dismiss sign-in info."]')))
            sing_in_element.click()
        except:
            ...

    #Exit of the site after the running program
    def __exit__(self, exc_type: type[BaseException] | None, exc: BaseException | None, traceback: TracebackType | None):
        if self.teardown:
            self.quit()
    
    #Change the currency of the site
    def change_currency(self, currency=None):
        wait = WebDriverWait(self, timeout=0.1)
        
        currency_element = self.find_element(By.CSS_SELECTOR, '[aria-controls="header_currency_picker"]')
        currency_element.click()

        selected_currency_element = self.find_element(By.XPATH, f'//div[text() = "{currency}"]')
        selected_currency_element.click()

        try:
            sing_in_element = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[aria-label="Dismiss sign-in info."]')))
            sing_in_element.click()
        except:
            ...

    #Select the place what the person type in the console
    def select_place_to_go(self, place_to_go):
        wait = WebDriverWait(self, timeout=0.1)

        search_field = self.find_element(By.NAME, "ss")
        search_field.clear()
        search_field.send_keys(place_to_go)

        first_result = wait.until(EC.element_to_be_clickable((By.XPATH, f'//div[text() = "{place_to_go}"]')))
        first_result.click()

    #Select the dates what the person type in the console 
    def select_dates(self, check_in_date, check_out_date):
        month_check_in = check_in_date[5] + check_in_date[6]
        month_check_out = check_out_date[5] + check_out_date[6]

        check_in_element = self.find_element(By.CSS_SELECTOR, f'[data-date="{check_in_date}"]')
        check_in_element.click()

        if int(month_check_out) > int(month_check_in)+1:
            for i in range((int(month_check_out)-1 ) - int(month_check_in)):
                next_month_button = self.find_element(By.CSS_SELECTOR, '[aria-label="Next month"]')
                next_month_button.click()

            check_out_element = self.find_element(By.CSS_SELECTOR, f'[data-date="{check_out_date}"]')
            check_out_element.click()
        elif int(month_check_out) < int(month_check_in):
            for i in range((int(month_check_out)+12) - int(month_check_in)):
                next_month_button = self.find_element(By.CSS_SELECTOR, '[aria-label="Next month"]')
                next_month_button.click()

            check_out_element = self.find_element(By.CSS_SELECTOR, f'[data-date="{check_out_date}"]')
            check_out_element.click()

    #Select the quantity of peoples in the travel 
    def select_adults(self, count):
        selection_element = self.find_element(By.CSS_SELECTOR, '[data-testid="occupancy-config"]')
        selection_element.click()

        adults_value_element = self.find_element(By.ID, 'group_adults')
        adults_value = adults_value_element.get_attribute('value')

        decrease_adults_element = self.find_element(By.XPATH, '//div[1]/div[@class="bfb38641b0"]/button[1]')

        for i in range(int(adults_value)-1):
            decrease_adults_element.click()
        
        selection_element.click()
        increase_adults_element = self.find_element(By.XPATH, '//div[1]/div[@class="bfb38641b0"]/button[2]')

        if int(adults_value) != 1:
            for i in range(count-1):
                increase_adults_element.click()

    #Click in the button Search
    def click_search(self):
        wait = WebDriverWait(self, timeout=0.1)
        search_button = self.find_element(By.XPATH, '//div[@class="e22b782521 d12ff5f5bf"]/button')
        search_button.click()

        try:
            sing_in_element = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[aria-label="Dismiss sign-in info."]')))
            sing_in_element.click()
        except:
            ...
    
    #Aplly some filters for facility the search
    def apply_filtrations(self):
        filtration = BookingFiltration(driver=self)
        filtration.aplly_star_rating(3, 4, 1)

        time.sleep(5)
        
        filtration.sort_price_lowest_first()

    #Print the results of the search
    def report_results(self):
        hotel_boxes = self.find_element(By.CSS_SELECTOR, '[class="dcf496a7b9 bb2746aad9"]')

        report = BookingReport(hotel_boxes)
        table = PrettyTable(
            field_names=["Hotel Name", 'Hotel Price', 'Hotel Score']
        )
        table.add_rows(report.pull_deal_box_attributes())
        print(table)