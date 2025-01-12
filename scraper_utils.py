import re
import os
import shutil
import requests


class ScraperUtils():

    def validate_inputs(self, number_of_pages_to_scrape: int, alias: str) ->str:
        if number_of_pages_to_scrape < 1 :
            message = "Received invalid number of pages to scrape: " + str(number_of_pages_to_scrape) + ". Enter valid number."
            print(message)
            return message
        if alias is not None and not self.__is_valid_url(alias):
            message = "Received invalid alias: " + alias + ". Enter valid url."
            print(message)
            return message
        return None

    def get_directory_path(self, page_number: int) -> str:
        images_folder = "images"
        if not os.path.exists(images_folder):
            os.makedirs(images_folder)
        sub_folder = "page_" + str(page_number)
        
        path = os.path.join(images_folder, sub_folder) 
        if os.path.exists(path):
            if os.path.isdir(path):  # Checking if the path is a directory
                shutil.rmtree(path, onerror=self.__handle_remove_readonly)  # Removing the directory and its contents
            else:
                os.remove(path)  # Removing the file if it's not a directory
        os.makedirs(path)
        return path

    def process_image(self, product_image, directory_path: str, image_count: int) -> str:
        if product_image:
            image_url = product_image["data-lazy-src"]

            # Downloading the image
            response = requests.get(image_url)
            file_path = None
            if response.status_code == 200:
                # Saving the image locally
                file_name = os.path.join(directory_path, "image" + str(image_count) + ".jpg")                
                with open(file_name, "wb") as file:
                    file.write(response.content)
                print("Image downloaded successfully as " + file_name)
                file_path = os.path.abspath(file_name)
                print(f"File saved at: {file_path}")
            else:
                print(f"Failed to download image. Status code: {response.status_code}")
        else:
            print("Image URL not found.")  
        return file_path


    def __handle_remove_readonly(self,func, path, exc_info):
        os.chmod(path, 0o777)  # Changing the file to be writable
        func(path)        


    def __is_valid_url(self, url: str) -> bool:
        # Using regular expression to check for a valid URL
        regex = re.compile(
            r'^(https?|ftp)://[^\s/$.?#].[^\s]*$', re.IGNORECASE
        )
        return re.match(regex, url) is not None
