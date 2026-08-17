from src.auth import RubikaAuth
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from src.extractor import DataExtractor
from src.analyzer import analyze
import tkinter as tk
import pandas
import json
import time

auth = RubikaAuth()

auth.login()

posts_data = []

# Offline Loading Menu
menu_choice = None

root = tk.Tk()
root.title("Rubika Menu")
root.geometry("300x120")

entry = tk.Entry(root, width=30)
entry.pack()

def skip(labeltext) :
    label = tk.Label(root, text=labeltext)
    label.pack(pady=10)


    button = tk.Button(root, text="Start", command=submit)
    button.pack(pady=10)

    root.mainloop()

    return menu_choice

def submit():
    global menu_choice
    menu_choice = entry.get()
    root.destroy()

skip("Enter your choice (1 for page scraping , 2 for analyzing) : ")

if menu_choice == "1" :
    # Page ID
    menu_choice = None

    root = tk.Tk()
    root.title("Rubika Menu")
    root.geometry("300x120")

    entry = tk.Entry(root, width=30)
    entry.pack()
    page_id = skip("Enter your page id : ")
    # Open Vitrin
    vitrin = WebDriverWait(auth.driver, 10).until(
        EC.presence_of_element_located(
            (
                By.XPATH,
                "//button[.//span[text()='ویترین']]"
            )
        )
    )
    time.sleep(2)
    vitrin.click()
    # Open Search
    WebDriverWait(auth.driver, 10).until(
        EC.presence_of_element_located(
            (
                By.XPATH,
                "//span[text()='جستجو']"
            )
        )
    ).click()
    # Type page id
    search = WebDriverWait(auth.driver, 10).until(
        EC.presence_of_element_located(
            (
                By.XPATH,
                "//input[@placeholder='جستجوی کاربر']"
            )
        )
    )
    search.clear()
    search.send_keys(page_id)

    # Wait for result
    try:
        WebDriverWait(auth.driver, 10).until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    f"//div[contains(text(),'{page_id}')]"
                )
            )
        ).click()
    except TimeoutError :
        print("Page id not found!")
        raise TimeoutError

    while True :
        # Finding the popup
        popup = WebDriverWait(auth.driver, 10).until(
            EC.presence_of_element_located(
                (
                    By.CSS_SELECTOR,
                     "div.rtl-l3f8vc"
                )
            )
        )
        # Only search inside the popup
        posts = popup.find_elements(
                By.CSS_SELECTOR,
                "div.rtl-lyl6cm"
                )
        WebDriverWait(popup, 20).until(
                    lambda d: any(
                        img.get_attribute("src")
                        for img in d.find_elements(By.TAG_NAME, "img")
                    )
                )   

        print("Posts in popup:", len(posts))

        for i in range(len(posts)):
            # Re-fetch every time because the DOM may refresh after clicking
            posts = popup.find_elements(
                By.CSS_SELECTOR,
                "div.rtl-lyl6cm"
                )
            print("Clicking post", i)

            auth.driver.execute_script(
                "arguments[0].click();",
                posts[i]
            )
            more = auth.driver.find_elements(
                        By.CSS_SELECTOR,
                        "span.rtl-9rhniv"
                    )

            print("Found:", len(more))
            if more:
                print(more[0].get_attribute("outerHTML"))
                auth.driver.execute_script(
                    "arguments[0].click();",
                    more[0]
                )
            time.sleep(0.5)
            extractor = DataExtractor(auth.driver)

            post = extractor.extract_current_post()
            posts_data.append(post)

            print(post)
            time.sleep(1)

            auth.driver.back()

            time.sleep(1)
        menu_choice = None

        root = tk.Tk()
        root.title("Rubika Menu")
        root.geometry("300x120")
    
        entry = tk.Entry(root, width=30)
        entry.pack()
        choice = skip("Press c to continue or q to quit : ")
        if choice == "q" :
            break

    with open("products.json", "w") as f:
        json.dump(posts_data, f)

    with open("products.json", "r") as f:
        posts_data = json.load(f)

    df = pandas.DataFrame(posts_data)

    df.to_csv(
        "products.csv",
        index=False,
        encoding="utf-8-sig"
    )
else :
    analyze()

analyze()

input("Press ENTER to quit ...")