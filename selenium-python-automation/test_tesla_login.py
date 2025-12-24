from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

import time

# Anti-detection options
options = webdriver.ChromeOptions()
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)
driver.maximize_window()

try:
    print("Opening Tesla account login...")
    driver.get("https://www.tesla.com/teslaaccount")  # Or https://auth.tesla.com if preferred
    wait = WebDriverWait(driver, 20)
    print("=== Tesla Login UI Automation Tests (Using Inspected Selectors) ===\n")
    passed = 0
    total = 5

    # Test 1: Email field present using exact ID you found
    print("Test 1: Email field is present. ( id='form-input-identity' ) ")
    try:
        email_field = wait.until(EC.presence_of_element_located((By.ID, "form-input-identity")))
        print("Result: PASSED\n")
        passed += 1
    except:
        print("Result: FAILED (email field not found)\n")

    # Test 2: Enter fake email
    print("Test 2: Enter fake email address")
    try:
        email_field.clear()
        email_field.send_keys("fake@test.com")
        print("Result: PASSED (email entered)\n")
        passed += 1
    except:
        print("Result: FAILED\n")
    # Test 3: Next button present using exact ID
    print("Test 3: Next button is present. ( id='form-submit-continue' ) ")
    try:
        next_button = wait.until(EC.element_to_be_clickable((By.ID, "form-submit-continue")))
        print("Result: PASSED\n")
        passed += 1
    except:
        print("Result: FAILED (Next button not found or not clickable)\n")

    # Test 4: Click Next (if button is clickable)
    print("Test 4: Click Next button")
    try:
        next_button.click()
        print("Result: PASSED (Next clicked)\n")
        passed += 1
    except:
        print("Result: FAILED (could not click Next - may be disabled initially)\n")
        
    # Test 5: Check if password field appears after Next (optional, flexible selector)
    print("Test 5: Password field appears after clicking Next")
    try:
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='password']")))
        print("Result: PASSED\n")
        passed += 1
    except:
        print("Result: FAILED or SKIPPED (password field not detected - common if fake email blocks flow)\n")
    print(f"=== Summary: {passed}/{total} tests PASSED ===\n")
    print("Browser staying open for review...")
finally:
    input("\nPress Enter in console to close browser...")
    driver.quit()
