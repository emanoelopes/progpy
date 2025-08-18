from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='automation.log'
)

def setup_driver():
    """Configure and return Firefox WebDriver"""
    options = webdriver.FirefoxOptions()
    # options.add_argument('--headless')  # Uncomment to run in headless mode
    return webdriver.Firefox(options=options)

def wait_for_element(driver, by, value, timeout=10):
    """Wait for element to be present and return it"""
    return WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((by, value))
    )

def automate_web_task():
    """Main automation function"""
    driver = None
    try:
        driver = setup_driver()
        logging.info("Browser started successfully")

        # Navigate to website
        url = "https://avamecinterativo.mec.gov.br"
        driver.get(url)
        logging.info(f"Navigated to {url}")

        # Fill login form
        login_field = wait_for_element(driver, By.CSS_SELECTOR, "input[type='text']")
        login_field.send_keys("emanoelcarvalho-lopes")
        
        password_field = wait_for_element(driver, By.CSS_SELECTOR, "input[type='password']")
        password_field.send_keys("U4JBQ-UQIXXU7W")
        logging.info("Login credentials entered")
        # Click login button
        login_button = wait_for_element(driver, By.CSS_SELECTOR, "button[type='submit']")
        driver.execute_script("arguments[0].scrollIntoView();", login_button)  # Scroll to the button
        time.sleep(1)  # Wait a bit before clicking
        logging.info("Clicking the login button")
        login_button.click()
        logging.info("Login submitted")
        time.sleep(5)  # Wait for login to complete

        # Pause for CAPTCHA
        print("Por favor, resolva o CAPTCHA manualmente.")
        print("Pressione Enter após resolver o CAPTCHA...")
        time.sleep(5)  # Wait for user to solve CAPTCHA
        
        # Continue with login after CAPTCHA is solved
        login_button = wait_for_element(driver, By.CSS_SELECTOR, "button[type='submit']")
        logging.info("Login button found, clicking to submit")
        driver.execute_script("arguments[0].scrollIntoView();", login_button)  # Scroll to the button
        time.sleep(1)  # Wait a bit before clicking
        logging.info("Clicking the login button")
        login_button.click()
        logging.info("Login submitted")

        # Navigate to the dashboard page
        dashboard_url = "https://avamecinterativo.mec.gov.br/app/dashboard/spaces/79547"
        driver.get(dashboard_url)
        logging.info(f"Navigated to dashboard: {dashboard_url}")
        time.sleep(5)  # Wait for the page to load


    except TimeoutException as e:
        logging.error(f"Timeout waiting for element: {e}")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
    finally:
        if driver:
            driver.quit()
            logging.info("Browser closed")

if __name__ == "__main__":
    # First, make sure you have Firefox and geckodriver installed:
    # sudo apt install firefox firefox-geckodriver
    
    automate_web_task()