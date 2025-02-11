import os
import subprocess
import time
import requests
import pytest
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture(scope="module", autouse=True)
def start_flask_app():
    """Starts the Flask app before tests and ensures cleanup after."""

    # Get the absolute path of app.py
    app_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "cards", "app.py"))

    # Start the Flask app with SocketIO
    process = subprocess.Popen(
        ["python", app_path],  # Run app.py directly to avoid import issues
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    def wait_for_server():
        """Waits until the Flask server is responsive."""
        for _ in range(2):  # Retry up to 10 times
            try:
                response = requests.get("http://localhost:5000/health_check", timeout=1)
                if response.status_code == 200:
                    return
            except requests.ConnectionError:
                time.sleep(1)  # Wait and retry

        # Print error output if Flask didn't start
        stderr_output = process.stderr.read()
        print("Flask failed to start. STDERR:\n", stderr_output)
        raise RuntimeError("Flask app did not start in time")

    try:
        wait_for_server()
        yield  # Run tests
    finally:
        process.terminate()
        process.wait()


@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()


def test_blackjack_hit_button(driver):
    # Start browser and navigate to the URL
    driver.get("http://localhost:5000/blackjack")  # URL where Flask app runs

    # Wait for the hit button to be present
    hit_button = WebDriverWait(driver, 2).until(
        EC.presence_of_element_located((By.ID, "hit-button-11111111-1111-1111-1111-111111111111-0"))
    )
    # Wait for the sum field to be present
    hand_sum_element = WebDriverWait(driver, 2).until(
        EC.presence_of_element_located((By.ID, "sum-11111111-1111-1111-1111-111111111111-0"))
    )
    hand_sum = hand_sum_element.text
    hit_button.click()

    hand_sum_after_click = hand_sum_element.text
    assert hand_sum <= hand_sum_after_click


def test_press_socket_testing_buttons(driver):
    # Start browser and navigate to the URL
    driver.get("http://localhost:5000/blackjack")  # URL where Flask app runs

    # Wait for the button and counter field
    socket_debugger_button_1, socket_debugger_button_1_counts = WebDriverWait(driver, 2).until(lambda d: (
        d.find_element(By.ID, "socket-debugger-button-1"),
        d.find_element(By.ID, "button1-count")
    ))

    # Scroll to the button before clicking
    ActionChains(driver).move_to_element(socket_debugger_button_1).perform()

    button_1_counts = socket_debugger_button_1_counts.text
    socket_debugger_button_1.click()
    button_1_counts_after_click = socket_debugger_button_1_counts.text

    assert button_1_counts < button_1_counts_after_click
