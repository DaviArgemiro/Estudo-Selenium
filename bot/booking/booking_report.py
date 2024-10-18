from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By

class BookingReport:
    def __init__(self, boxes_section_element: WebDriver):
        self.boxes_section_element = boxes_section_element
        self.deal_boxes = self.pull_deal_boxes()

    def pull_deal_boxes(self):
        return self.boxes_section_element.find_elements(By.CSS_SELECTOR, '[data-testid="property-card"]')
    
    def pull_deal_box_attributes(self):
        collection = []

        for deal_box in self.deal_boxes:
            #Pulling the hotel name
            hotel_name = deal_box.find_element(By.CSS_SELECTOR,
            '[data-testid="title"]').get_attribute('innerHTML').strip()

            hotel_price = deal_box.find_element(By.CSS_SELECTOR, 
            '[data-testid="price-and-discounted-price"]').get_attribute('innerHTML').strip()

            hotel_score = deal_box.find_element(By.XPATH, 
            '//div[@data-testid="review-score"]/div[@class="a3b8729ab1 d86cee9b25"]/div[@class="ac4a7896c7"]').text


            collection.append(
                [hotel_name, hotel_price, hotel_score]
            )

        
        return collection