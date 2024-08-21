import unittest
from unittest.mock import patch, MagicMock
from .appium_test import run_appium_test


class AppiumTest(unittest.TestCase):
    @patch("appium_test.webdriver.Remote")
    def test_run_appium_test(self, MockWebDriver):
        # Mock the WebDriver instance
        mock_driver = MockWebDriver.return_value

        mock_driver.start_recording_screen.return_value = None
        mock_driver.save_screenshot.return_value = None
        mock_driver.page_source = "<hierarchy><node/></hierarchy>"
        mock_driver.stop_recording_screen.return_value = b"video_data"

        ui_hierarchy, screen_changed = run_appium_test(
            apk_path="apks/test.apk",
            first_screenshot_path="screenshots/first_screenshot.png",
            second_screenshot_path="screenshots/second_screenshot.png",
            video_path="videos/video.mp4",
        )

        self.assertEqual(ui_hierarchy, "<hierarchy><node/></hierarchy>")
        self.assertFalse(screen_changed)
        MockWebDriver.assert_called_once_with(
            "http://127.0.0.1:4723",
            {
                "platformName": "Android",
                "platformVersion": "11",
                "deviceName": "tcp:5037",
                "app": "apks/test.apk",
                "automationName": "UiAutomator2",
                "autoGrantPermissions": True,
                "noReset": True,
                "newCommandTimeout": 600,
            },
        )
        mock_driver.save_screenshot.assert_any_call("screenshots/first_screenshot.png")
        mock_driver.save_screenshot.assert_any_call("screenshots/second_screenshot.png")
        mock_driver.stop_recording_screen.assert_called_once()


if __name__ == "__main__":
    unittest.main()
