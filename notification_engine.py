from abc import ABC, abstractmethod
import os
import json

class NotificationEngine(ABC):
    
    @abstractmethod
    def notify(self):
        pass

class NotifyViaConsole(NotificationEngine):
    def notify(self, number_of_records: int, time_stamp_string: str) -> str:
        message = "Number of products scraped and updated during the session ended at " + time_stamp_string + " is " + str(number_of_records)
        print(message)
        return message