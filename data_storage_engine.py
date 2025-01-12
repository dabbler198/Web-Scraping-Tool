from abc import ABC, abstractmethod
import os
import json

class DataStorageEngine(ABC):
    
    @abstractmethod
    def store_data(self):
        pass

class LocalDataStorageEngine(DataStorageEngine):
    def store_data(self, data_to_store: list, time_stamp_string: str):
        images_folder = "output"
        if not os.path.exists(images_folder):
            os.makedirs(images_folder)
        time_stamp_string = time_stamp_string.replace(":","_")
        file_path = os.path.join(images_folder, 'ScrapeResults ' + time_stamp_string + ".json")
        with open(file_path, "w") as file:
            json.dump(data_to_store, file)        



