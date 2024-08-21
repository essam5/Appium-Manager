import time
from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction
import os


def run_appium_test(
    apk_path, first_screenshot_path, second_screenshot_path, video_path
):
    # Desired capabilities for the Android Emulator
    desired_caps = {
        "platformName": "Android",
        "platformVersion": "11",
        "deviceName": "tcp:5037",
        "app": apk_path,
        "automationName": "UiAutomator2",
        "autoGrantPermissions": True,
        "noReset": True,
        "newCommandTimeout": 600,
    }

    # Start the Appium session
    driver = webdriver.Remote("http://127.0.0.1:4723", desired_caps)

    driver.start_recording_screen()

    # Wait for the app to launch
    time.sleep(5)

    driver.save_screenshot(first_screenshot_path)

    # Find the first button using its resource ID or other properties
    button = driver.find_element_by_xpath("//android.widget.Button[1]")

    # Simulate a click on the first button
    TouchAction(driver).tap(button).perform()

    # Wait for any potential screen change
    time.sleep(3)

    driver.save_screenshot(second_screenshot_path)

    # Capture the UI hierarchy
    ui_hierarchy = driver.page_source

    # Check if the screen has changed
    screen_changed = ui_hierarchy != driver.page_source

    video_data = driver.stop_recording_screen()
    with open(video_path, "wb") as video_file:
        video_file.write(video_data)

    driver.quit()

    return ui_hierarchy, screen_changed
