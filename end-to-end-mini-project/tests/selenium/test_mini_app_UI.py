from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import time

# Setup Chrome with anti-detection
options = webdriver.ChromeOptions()
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)

print("Setting up Chrome driver...")

try:
    service = Service(ChromeDriverManager().install())
    print("ChromeDriver downloaded/installed successfully")
except Exception as e:
    print("ERROR downloading ChromeDriver:", e)
    input("Press Enter to exit...")
    exit()

try:
    driver = webdriver.Chrome(service=service, options=options)
    print("Chrome browser launched successfully")
except Exception as e:
    print("ERROR launching Chrome:", e)
    input("Press Enter to exit...")
    exit()

driver.maximize_window()

try:
    print("=== Selenium UI Tests for Mini-App - ToDo List ===\n")
    driver.get("http://127.0.0.1:5000")
    wait = WebDriverWait(driver, 10)
    tasks_to_add = ["Check battery health", "Rotate tires", "Schedule service"]
    print(f"Adding {len(tasks_to_add)} tasks via UI...\n")
    for task in tasks_to_add:
    # Find input and type task
        input_field = wait.until(EC.element_to_be_clickable((By.ID, "taskInput")))
        input_field.clear()
        input_field.send_keys(task)
    # Click Add button
        add_button = driver.find_element(By.ID, "addButton")
        add_button.click()
    # Brief wait for list update
        time.sleep(2)
    # Assert all tasks appear in list
    list_items = driver.find_elements(By.CSS_SELECTOR, "#todoList li")
    print(f"Found {len(list_items)} tasks in list after adding")
    assert len(list_items) >= len(tasks_to_add)
    displayed_tasks = [item.text.strip() for item in list_items]
    for task in tasks_to_add:
        assert task in displayed_tasks
        print(f"✓ '{task}' visible in list")
    print("\nAll tasks added and visible - PASSED\n")
    # Test persistence on refresh
    print("Refreshing page to test persistence...")
    driver.refresh()
    time.sleep(2)
    list_items_after = driver.find_elements(By.CSS_SELECTOR, "#todoList li")
    assert len(list_items_after) >= len(tasks_to_add)
    print(f"Tasks persist after refresh: {len(list_items_after)} found - PASSED")
    print("\n=== All Selenium UI tests PASSED ===\n")

finally:
    input("Press Enter to close browser...")
    driver.quit()
