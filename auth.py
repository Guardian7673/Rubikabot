from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import json
import os
import time

path = os.getcwd() + r"\chromedriver.exe"

class RubikaAuth:

    def __init__(self):

        self.cookies_file = "cookies/session.pkl"

        options = Options()

        self.driver = webdriver.Chrome(
            service=Service(path),
            options=options
        )

    def save_values(self):
        session = {
            "auth": self.driver.execute_script(
                "return localStorage.getItem('auth');"
            ),
            "profile": self.driver.execute_script(
                "return localStorage.getItem('profile');"
            )
        }

        with open("session.json", "w") as f:
            json.dump(session, f)
            
        print("[+] Authentication keys saved")

    def load_values(self):

        if not os.path.exists("session.json"):
                    return False

        with open("session.json", "r") as f:
            session = json.load(f)

        if session["auth"] == None or session["profile"] == None :
                    return False
        
        self.driver.get("https://m.rubika.ir")

        self.driver.execute_script(
            "localStorage.setItem('auth', arguments[0]);",
            session["auth"]
        )

        self.driver.execute_script(
            "localStorage.setItem('profile', arguments[0]);",
            session["profile"]
        )

        self.driver.refresh()

        print("[+] Authentication keys loaded")

        return True

    def login(self):

        self.driver.get(
            "https://m.rubika.ir"
        )

        if self.load_values():

            print("[+] Logged in using session")
            return

        print()
        print("Please login manually")
        print("You have 60 seconds")

        time.sleep(60)

        self.save_values()

        print("[+] Login complete")

