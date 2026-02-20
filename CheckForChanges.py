import os.path
from glob import glob
from datetime import datetime
from selenium import webdriver
from selenium.common import TimeoutException, ElementClickInterceptedException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from dotenv import load_dotenv
from Const import DEFAULT_TIMEOUT
from Const import LINK
from Const import XPATHS
from Const import FILE_PATH
from Const import IMAGE_PATH

def wait_for_elements_to_be_clickable(driver, xpath, timeout = DEFAULT_TIMEOUT):
    try:
        wait = WebDriverWait(driver, timeout)
        element = wait.until(expected_conditions.element_to_be_clickable((By.XPATH, xpath)))
        return element
    except TimeoutException as error:
        print(f"Element: {xpath} not available after {timeout}s")
        print(f"Error: {error}")

def wait_and_click(driver, xpath, timeout = DEFAULT_TIMEOUT):
    try:
        element = wait_for_elements_to_be_clickable(driver, xpath, timeout)
        element.click()
    except (ElementClickInterceptedException, ElementClickInterceptedException) as error:
        print("Error during click")
        print(f"Error: {error}")

def wait_and_type(driver, xpath, keys, timeout = DEFAULT_TIMEOUT):
    try:
        element = wait_for_elements_to_be_clickable(driver, xpath, timeout)
        element.clear()
        element.send_keys(keys)
    except Exception as error:
        print("Error during typing process")
        print(f"Error: {error}")

def wait_and_act(driver, xpath, keys=None , timeout = DEFAULT_TIMEOUT):
    if keys is not None:
        wait_and_type(driver, xpath, keys, timeout = timeout)
    else:
        wait_and_click(driver, xpath, timeout = timeout)

def get_latest_topic(driver, xpath, file_path = FILE_PATH, timeout = DEFAULT_TIMEOUT):
    try:
        element = wait_for_elements_to_be_clickable(driver, xpath, timeout = timeout)
        title = element.get_attribute("title")
        link = element.get_attribute("href")
        changes_happened, file_existed = save_new_topic(title, link, file_path)
        if changes_happened:
            remove_previous_screenshots()
            take_screenshot(driver, element)
        notify(changes_happened, file_existed, title, link)
    except Exception as error:
        print("Error in getting the latest topic")
        print(f"Error: {error}")

def highlight_element(driver, element, border="3px solid red"):
    driver.execute_script("arguments[0].style.border = arguments[1];", element, border)

def take_screenshot(driver, element, image_path = IMAGE_PATH):
    highlight_element(driver, element)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    driver.save_screenshot(f"{image_path}_{timestamp}.png")

def remove_previous_screenshots(image_path = IMAGE_PATH):
    for file in glob(f"{image_path}*.png"):
        try:
            os.remove(file)
        except Exception as error:
            print("Error removing file")
            print(f"Error: {error}")

def save_new_topic(title, link, file_path = FILE_PATH):
    try:
        write_to_file = True
        file_existed = False
        if os.path.exists(file_path):
            file_existed = True
            with open(file_path, "r" , encoding="utf-8") as file:
                lines = file.read().splitlines()
                if len(lines) == 2 and (lines[0] == title or lines[1] == link):
                    write_to_file = False
        if write_to_file:
            with open(file_path, "w" , encoding="utf-8") as file:
                file.write(f"{title}\n{link}\n")
            if file_existed:
                return True, True
            else:
                return True, False
        else:
            return False, True
    except Exception as error:
        print("Error during saving process")
        print(f"Error: {error}")

def notify(changes_happened, file_existed, title ,link):
    if changes_happened and file_existed:
        print("Latest topic HAS changed! :)")
    elif not changes_happened and file_existed:
        print("Latest topic HAS NOT changed! :(")
    else:
        print("Saved latest topic: :|")
    print(f"Title: {title}")
    print(f"Link: {link}")


def main():
    driver = webdriver.Chrome()
    try:
        load_dotenv()
        account_email = os.getenv("EMAIL")
        account_password = os.getenv("PASSWORD")
        driver.get(LINK)
        wait_and_act(driver, XPATHS.OPENID)
        wait_and_act(driver, XPATHS.EMAIL , account_email)
        wait_and_act(driver, XPATHS.NEXT)
        wait_and_act(driver, XPATHS.PASSWORD, account_password)
        wait_and_act(driver, XPATHS.SIGN_IN)
        wait_and_act(driver, XPATHS.NO)
        get_latest_topic(driver, XPATHS.DISCUSSION)
    except Exception as error:
        print("Unexpected error")
        print(f"Error: {error}")
    finally:
        driver.quit()

main()