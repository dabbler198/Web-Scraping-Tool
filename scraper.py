from bs4 import BeautifulSoup
import requests
from datetime import datetime
from retrying import retry
from data_storage_engine import LocalDataStorageEngine
from notification_engine import NotifyViaConsole
from scraper_utils import ScraperUtils

local_data_storage_engine = LocalDataStorageEngine()
notify_via_console_engine = NotifyViaConsole()
scraper_utils = ScraperUtils()

class Scraper():
    
    def scrape_data(self, number_of_pages_to_scrape: int, alias: str) -> str:
        validation_result = scraper_utils.validate_inputs(number_of_pages_to_scrape, alias)
        if validation_result is not None:
            return validation_result

        scrape_results = []
        for i in range(1, number_of_pages_to_scrape+1):
            try:
                page_result = self.__scrape_data_helper(i, alias)
                scrape_results.extend(page_result)
            except RuntimeError as e:
                print(f"Error occurred while fetching details for page number: {i}")
        
        current_time = datetime.now()
        current_time_str = current_time.strftime("%Y-%m-%d_%H:%M:%S")
        local_data_storage_engine.store_data(scrape_results, current_time_str)
        return notify_via_console_engine.notify(len(scrape_results), current_time_str)


    @retry(wait_exponential_multiplier=1000, wait_exponential_max=5000, 
       retry_on_exception=lambda x: isinstance(x, RuntimeError))
    def __scrape_data_helper(self, page_number: int, alias: str) -> list:
        url = f'https://dentalstall.com/shop/page/{page_number}'
        proxies = None
        if alias is not None:
            proxies = {
                "http": alias,
                "https": alias
            }
        pageToScrape = requests.get(url, proxies=proxies)

        if pageToScrape.status_code == 200:
            soup = BeautifulSoup(pageToScrape.text, "html.parser")

            pageResults = []
            products = soup.findAll('div', attrs = {'class':'product-inner'})
            directory_path = scraper_utils.get_directory_path(page_number)
            image_count = 0

            for product in products:
                product_title = product.find('h2', attrs = {'class':'woo-loop-product__title'})
                product_price = product.find('span', attrs = {'class':'woocommerce-Price-amount amount'})
                product_image = product.find('img', {'data-lazy-src': True})
                path_to_image = scraper_utils.process_image(product_image, directory_path, image_count)
                image_count = image_count + 1
                
                item = {
                    'product_title' : product_title.text,
                    'product_price' : product_price.text,
                    'path_to_image' : path_to_image
                }      
                pageResults.append(item)                
            return pageResults
        else:
            print(f"Failed to fetch page details. Status code: {pageToScrape.status_code}")
            raise RuntimeError("An unexpected error occurred while fetching details for page number: ", page_number, " exception: ", e)
