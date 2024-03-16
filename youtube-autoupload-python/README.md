# youtube-autoupload-bot
This is a python/selenium script that can help you to upload videos in your youtube automatically.


change the chromedriver.exe with the latest one AND CHANGE THE PATHS OF



options.add_argument("user-data-dir=C:\\Users\\User\\AppData\\Local\Google\\Chrome Beta\\User Data\\")
options.binary_location = "C:\\Program Files\\Google\\Chrome Beta\\Application\\chrome.exe"

but double backslace


======================================================================================================

YouTube Auto-Upload Bot Documentation
Overview
The YouTube Auto-Upload Bot is a Python script utilizing Selenium that automates the process of uploading videos to YouTube. This documentation provides step-by-step instructions on how to set up and use the bot.

Prerequisites
Python: Ensure Python is installed on your system. You can download it from python.org.

Selenium: Install Selenium using pip:

pip install selenium
Chrome Browser: The script is designed to work with the Chrome browser. Make sure you have Chrome installed on your system.

ChromeDriver: Download the latest ChromeDriver compatible with your Chrome version. You can find it at chromedriver.chromium.org. Replace the existing chromedriver.exe in the script's directory with the downloaded one.

Configuration
Chrome User Profile:

Find your Chrome user profile directory. 

C:\Users\User\AppData\Local\Google\Chrome Beta\User Data\
Update the user-data-dir option in the script with your profile directory:
python

options.add_argument("user-data-dir=C:\\Users\\User\\AppData\\Local\\Google\\Chrome Beta\\User Data\\")
Chrome Binary Location:


C:\Program Files\Google\Chrome Beta\Application\chrome.exe
Update the binary_location option in the script with your Chrome binary location:
python

options.binary_location = "C:\\Program Files\\Google\\Chrome Beta\\Application\\chrome.exe"
ChromeDriver Path:

Update the chrome_driver_path variable in the script with the path to your ChromeDriver executable:
python

chrome_driver_path = "C:\\path\\to\\chromedriver.exe"
Usage
Prepare Video: Make sure your video file is ready for upload and located in a directory accessible by the script.

Run the Script: Execute the script using Python:


python youtube_autoupload_bot.py
Follow Script Prompts: The script will guide you through the upload process, prompting for necessary information such as video title, description, tags, etc.

Sit Back and Relax: Once started, the script will handle the entire upload process automatically.

Notes
Ensure stable internet connection during the upload process.
Test the script with a test YouTube account before using it with your main account.
Always keep your Chrome browser and ChromeDriver up to date for compatibility.
Troubleshooting
If you encounter any issues, refer to the error messages displayed in the terminal for troubleshooting.
Double-check the configuration steps to ensure all paths and settings are correct.
