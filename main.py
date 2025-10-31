from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import ElementClickInterceptedException
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import load_dotenv
import os
import time

# --- 1. LOAD ENVIRONMENT VARIABLES ---
# This loads the .env file from your project directory
# so os.getenv() can access the values.
load_dotenv()

# Get variables from the environment using os.getenv()
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")
SIMILAR_ACCOUNT = os.getenv("SIMILAR_ACCOUNT")


class InstaFollower:
    def __init__(self):
        chrome_options = webdriver.ChromeOptions()
        # This option keeps the Chrome browser open after the script finishes
        # (useful for debugging)
        chrome_options.add_experimental_option("detach", True)

        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()), 
            options=chrome_options
        )

    def login(self):
        """Navigates to the login page, enters credentials, and handles popups."""
        self.driver.get("https://www.instagram.com/accounts/login/")
        
        # Wait for the login page to load fully
        time.sleep(5)
        
        # Find username and password fields
        username_input = self.driver.find_element(By.XPATH, '//*[@id="loginForm"]/div[1]/div[1]/div/label/input')
        password_input = self.driver.find_element(By.XPATH, '//*[@id="loginForm"]/div[1]/div[2]/div/label/input')

        # Enter credentials
        username_input.send_keys(USERNAME)
        password_input.send_keys(PASSWORD)

        # Pause briefly before submitting
        time.sleep(1.5)

        # Submit the login form
        password_input.send_keys(Keys.ENTER)
        
        # Wait for login to process and the main page to load
        time.sleep(7.1)

        # --- Handle "Save Login Info?" Popup ---
        # NOTE: This will crash if the button isn't found.
        # A try...except block would be safer here.
        save_login_button = self.driver.find_element(By.XPATH, value="//div[contains(text(), 'Not now')]")
        if save_login_button:
            save_login_button.click()

        # Wait for the next popup to potentially appear
        time.sleep(4.1)

        # --- Handle "Turn on Notifications?" Popup ---
        # NOTE: This will also crash if the button isn't found.
        notifications_button = self.driver.find_element(By.XPATH, value="//div[contains(text(), 'OK')]")
        if notifications_button:
            notifications_button.click()

        # Wait for the page to settle
        time.sleep(1.8)

    def find_followers(self):
        """Navigates to the target account's profile and opens their followers list."""
        self.driver.get(f"https://www.instagram.com/{SIMILAR_ACCOUNT}/")

        # Wait for the profile page to load
        time.sleep(5)

        # Find and click the "followers" link
        followers_button = self.driver.find_element(By.XPATH, "//a[contains(@href, '/followers/')]")
        followers_button.click()

        # Wait for the followers modal (popup) to open
        time.sleep(3)
    
        # Find the scrollable followers list modal
        # This uses two different XPaths as a fallback
        try:
            # First, try a very specific (and brittle) absolute XPath
            modal = self.driver.find_element(
                By.XPATH, '/html/body/div[4]/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[2]'
            )
        except:
            # If that fails, try a more robust, class-based XPath
            modal = self.driver.find_element(
                By.XPATH, "//div[@role='dialog']//div[contains(@class, '_aano')]"
            )

        # Scroll down inside the modal to load more followers
        for i in range(5):
            # Use JavaScript to scroll the modal element to its full height
            self.driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", modal)
            # Wait for new followers to load after scrolling
            time.sleep(2)

    def follow(self):
        """Finds all 'Follow' buttons in the modal and clicks them."""
        
        # Pause before starting to follow
        time.sleep(3)

        # Find all buttons that explicitly say "Follow" inside the modal
        follow_buttons = self.driver.find_elements(By.XPATH, "//div[@role='dialog']//button[.//div/div[text()='Follow']]")

        for i, button in enumerate(follow_buttons):
            try:
                # Scroll the button into view just in case it's not visible
                self.driver.execute_script("arguments[0].scrollIntoView(true);", button)
                
                # Brief pause after scrolling
                time.sleep(0.5)

                button.click()

                # Wait for the follow action to register
                time.sleep(1.5)
                
            except ElementClickInterceptedException:
                # This happens if a popup appears (e.g., "Are you sure?")
                # or if the click is otherwise blocked.
                print(f"Could not click button {i} due to interception.")
                try:
                    # Look for a "Cancel" button on the new popup and click it
                    cancel_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Cancel')]")
                    cancel_button.click()
                    time.sleep(1)
                except:
                    # If no "Cancel" button, just move on
                    pass
            except Exception as e:
                # Catch any other errors
                print(f"An error occurred on button {i}: {e}")
                    
    def close_chrome(self):
        """Closes the browser session."""
        self.driver.quit()


# --- 2. RUN THE BOT ---
if not all([USERNAME, PASSWORD, SIMILAR_ACCOUNT]):
    print("Error: Missing environment variables.")
    print("Please ensure you have a .env file with USERNAME, PASSWORD, and SIMILAR_ACCOUNT.")
else:
    print("Bot starting...")
    bot = InstaFollower()
    
    print("Logging in...")
    bot.login()
    
    print(f"Finding followers of {SIMILAR_ACCOUNT}...")
    bot.find_followers()
    
    print("Following users...")
    bot.follow()
    
    print("Closing browser...")
    bot.close_chrome()
    
    print("Bot run complete.")