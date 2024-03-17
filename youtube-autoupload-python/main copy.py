import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By

# options.add_experimental_option('excludeSwitches', ['enable-logging'])


options = webdriver.ChromeOptions()
chrome_driver_path = "C:\\Automate\\AI-Automation-Video-Generating\\youtube-autoupload-python\\chromedriver.exe"
options.add_argument("--log-level=3")
options.add_argument("user-data-dir=C:\\Users\\lenovo\\AppData\\Local\\Google\\Chrome Beta\\User Data\\")
options.binary_location = "C:\\Program Files\\Google\\Chrome Beta\\Application\\chrome.exe"

print("\033[1;31;40m : Welcome In Auto Uploading Video... ")
time.sleep(5)

dir_path = 'Generated Videos/Love/'

for i, filename in enumerate(os.listdir(dir_path), start=1):
    if filename.endswith('.mp4'):
        bot = webdriver.Chrome(options=options)
        bot.get("https://studio.youtube.com")
        time.sleep(3)
        upload_button = bot.find_element(By.XPATH, '//*[@id="upload-icon"]')
        upload_button.click()
        time.sleep(1)

        file_input = bot.find_element(By.XPATH, '//*[@id="content"]/input')
        abs_path = os.path.abspath(os.path.join(dir_path, filename))
        file_input.send_keys(abs_path)

        time.sleep(7)

        # Set the title using JavaScript
        title = "Your Video Title Here"  # Replace with your desired title
        title_element = bot.find_element(By.ID, 'textbox')
        bot.execute_script("arguments[0].textContent = arguments[1];", title_element, title)

        # Set the video description
        description = "Your detailed video description goes here."  # Replace with your desired description
        description_div = bot.find_element(By.XPATH, '//div[@id="textbox" and @aria-label="Tell viewers about your video (type @ to mention a channel)"]')
        bot.execute_script("arguments[0].textContent = arguments[1];", description_div, description)
 
        # "Show More" button ko locate karna
        show_more_button = bot.find_element(By.XPATH, '//ytcp-button[@id="toggle-button"]//div[contains(text(),"Show more")]')

        # Button par click karna
        show_more_button.click()

        # Thoda wait karna taaki page ke elements load ho jaye
        time.sleep(2)  # Adjust this delay according to your network speed or page response time

        # Set the video tags
        tags = "tag1, tag2, tag3"  # Replace with your desired tags, separated by commas
        # Locate the tags input based on your provided structure
        tags_input = bot.find_element(By.XPATH, '//*[@id="text-input"]')
        tags_input.send_keys(tags)

        next_button = bot.find_element(By.XPATH, '//*[@id="next-button"]')
        for _ in range(3):
            next_button.click()
            time.sleep(1)

        done_button = bot.find_element(By.XPATH, '//*[@id="done-button"]')
        done_button.click()
        time.sleep(5)
        bot.quit()
