
from selenium import webdriver
from datetime import datetime

import chromedriver_autoinstaller
import copy
import sys
import time
import random
import os


class BBAssistant():
    def __init__(self):
        self.intervals = self.get_intervals()
        self.driver = self.get_driver()
        super().__init__()

    def get_bb_slot(self, url):
    
        self.driver.get(url)     
        time.sleep(2)
        print("Trying to find a slot!")
        try:
            self.driver.find_element_by_xpath("//button[@id = 'checkout']").click()
            time.sleep(5)  #driver take a few sec to update the new url
            src = self.driver.page_source
            if "checkout" in self.driver.current_url and not "Unfortunately, we do not have" in src:
                print("Found the slots!")
                for i in range(60):
                        notify("Slots Available!", "Please go and choose the slots!")
                        time.sleep(20)
        except Exception  as e:
            print("If this message pops up multiple times, please find the error and create a PR!")
            print (e)
            pass
        print("No Slots found. Will retry again.")
        time.sleep(50)
        return

    def notify(self, title, text):
        if os.name == 'posix':
            os.system("""
                osascript -e 'display notification "{}" with title "{}"'
                """.format(text, title))
            os.system('say "Slots for delivery available!"')
        elif os.name == 'Linux':
            os.system('spd-say "Slots for delivery available!"')

    # def display_intervals(self):
    #     print("Time is displayed in 24 hour format")
    #     print("Will try checkout at the following intervals:")
    #     for key, value in self.intervals.items():
    #         for minute in value:
    #             print("At: %s:%s" % (key, minute))

    def get_intervals(self):
        intervals = dict()
        hour_part_1 = range(0, 31)
        hour_part_2 = range(31, 61)
        for i in range(6,24):
            number_of_tries = random.randrange(2, 5)
            attempts_for_hour = []
            for attempt in range(0, number_of_tries):
                non_zero_attempt = attempt + 1
                attempts_left = number_of_tries - non_zero_attempt
                if attempts_left >= 1:
                    minute = random.sample(hour_part_1, 1)[0]
                else:
                    minute = random.sample(hour_part_2, 1)[0]
                attempts_for_hour.append(minute)
            intervals.update({
                str(i): attempts_for_hour
            })
        return intervals

    def get_driver(self):
        # auto-install chromedriver 
        chromedriver_autoinstaller.install() 
        driver = webdriver.Chrome()
        return driver

    def checkout_at_intervals(self):
        today = datetime.now()
        while datetime.now().day == today.day:
            now = datetime.now()
            this_hour = str(now.hour)
            if this_hour in self.intervals.keys():
                attempts_for_hour = copy.copy(
                    self.intervals.get(this_hour)
                )
                this_minute = now.minute
                if this_minute in attempts_for_hour:
                    get_bb_slot(url, driver)
                    position_in_list = attempts_for_hour.index(this_minute)
                    attempts_for_hour.pop(position_in_list)


    def start(self):
        url = 'https://www.bigbasket.com/basket/?ver=1'
        self.driver.get(url)
        print("Please login using OTP and then wait for a while.")
        self.checkout_at_intervals()


bb_assistant = BBAssistant()
bb_assistant.start()
