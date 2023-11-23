import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import random
import string
import time
from selenium.common.exceptions import TimeoutException


@pytest.fixture
def browser():
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()


def generate_random_number():
    return ''.join(random.choices(string.digits, k=4))

# Test Case 2: Login to Gumtree and Edit Ad
def test_edit_gumtree_ad(browser):

    browser.get("https://www.gumtree.co.za")


    wait = WebDriverWait(browser, 30)  # Increased timeout to 30 seconds


    login_to_gumtree(browser, wait)


    navigate_to_my_ads(browser, wait)

    edit_ad(browser, wait)


    current_title = capture_and_verify_title(browser, wait)

    # Generate a random 4-digit number
    random_number = generate_random_number()

    # Append the random number to the current title
    new_title = f"{current_title} {random_number}"

    # Update the ad title
    update_ad_title(browser, wait, new_title)

    # Save the changes
    save_changes(browser, wait)

    # Logout from Gumtree
    logout_from_gumtree(browser, wait)


    time.sleep(10)


def login_to_gumtree(browser, wait):

    element = browser.find_element(By.XPATH, "//span[@class='auth-nav-link sign-in']")
    element.click()

    header_element = wait.until(
        EC.visibility_of_element_located((By.XPATH, "//header[@class='full-page-modal-header-area']"))
    )
    assert header_element.is_displayed(), "Pop-up with header is not displayed"


    username_input = browser.find_element(By.XPATH,
                                         "//div[@class='login-email-field input-wrapper']//input[@type='text']")
    password_input = browser.find_element(By.XPATH,
                                         "//div[@class='login-pwd-field input-wrapper']//input[@type='password']")


    wait.until(EC.visibility_of(username_input))
    wait.until(EC.visibility_of(password_input))


    username_input.send_keys("gumtreesaautomation@gmail.com")
    password_input.send_keys("Gumtr33@SA")

    login_button = browser.find_element(By.XPATH, "//button[normalize-space()='Log In']")
    login_button.click()


    pro_click = wait.until(EC.visibility_of_element_located((By.XPATH, "//*[@id='dropdown-menu-button']")))
    pro_click.click()

def navigate_to_my_ads(browser, wait):

    myads = wait.until(EC.visibility_of_element_located((By.XPATH, "//*[@id='dropdown-holder']/ul/li[3]")))
    scroll_to_element(browser, myads)
    myads.click()


    ad_elements = wait.until(
        EC.presence_of_all_elements_located((By.XPATH, "//*[@id='wrapper']/section/div[3]/div[1]/div/div[1]/div"))
    )
    assert len(ad_elements) > 0, "No ads are displayed on the My Ads page"

def edit_ad(browser, wait):
    try:

        editad = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//*[@id='wrapper']/section/div[3]/div[3]/div/div[2]/div/div[1]/div[1]/div[3]/div[1]/a/span[2]")))
        scroll_to_element(browser, editad)
        editad.click()


        browser.save_screenshot("editad_popup")


        popup_element = wait.until(EC.visibility_of_element_located((By.XPATH, "//*[@id='wrapper']/div[2]/div[5]/div[1]/div/h1")))
        assert popup_element.is_displayed(), "Pop-up dialog is not displayed"


        skip_button = browser.find_element(By.XPATH, "//*[@id='wrapper']/div[2]/div[5]/div[1]/div/span[2]/a")


        skip_button.click()

    except TimeoutException as e:
        # Handle timeout exception
        print(f"TimeoutException: {e}")
        browser.save_screenshot("timeout_exception_edit_ad.png")
        raise  # re-raise the exception to fail the test

def capture_and_verify_title(browser, wait):
    # Find the element representing the title of the ad using its XPath
    title_element = wait.until(EC.visibility_of_element_located(
        (By.XPATH, "//*[@id='wrapper']/div[2]/div[4]/div[1]/div[2]/div[1]/span")))
    browser.save_screenshot("screuen.png")


    current_title = title_element.text
    return current_title

def update_ad_title(browser, wait, new_title):

    title_input_element = browser.find_element(By.XPATH, "//*[@id='wrapper']/div[2]/div[4]/div[1]/div[2]/div[1]/span")
    browser.save_screenshot("scrheen.png")


    title_input_element.clear()
    title_input_element.send_keys(new_title)

def save_changes(browser, wait):
    browser.find_element(By.XPATH, "//*[@id='wrapper']/div[2]/div[4]/div[19]/div").click()

def logout_from_gumtree(browser, wait):
    pro_click = wait.until(EC.visibility_of_element_located((By.XPATH, "//*[@id='dropdown-menu-button']")))
    pro_click.click()
    time.sleep(10)
    browser.find_element(By.XPATH, "//*[@id='dropdown-holder']/ul/li[10]/a/span").click()
    time.sleep(5)

def scroll_to_element(browser, element):
    browser.execute_script("arguments[0].scrollIntoView(true);", element)
    time.sleep(1)



































