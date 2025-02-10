import pytest
import subprocess
import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# TODO: get this working. It works when the application is *already* running (I can see it clicking the websocket
#  button), but I can't get it to spin up the application.
@pytest.fixture(scope="module", autouse=True)
def start_flask_app():
    # Set the FLASK_APP environment variable
    os.environ['FLASK_APP'] = 'app:create_app'
    # Start the Flask app
    process = subprocess.Popen(["flask", "run"])
    # Wait for the Flask app to start
    time.sleep(2)
    yield
    # Terminate the Flask app
    process.terminate()


@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()


@pytest.mark.skip(reason="Skipping until selenium can launch the application.")
def test_blackjack_hit_button(driver):
    # Start browser and navigate to the URL
    driver.get("http://localhost:5000/blackjack")  # URL where Flask app runs

    # Wait for the hit button to be present
    hit_button = WebDriverWait(driver, 2).until(
        EC.presence_of_element_located((By.ID, "hit-button"))
    )
    hit_button.click()

    # Verify the output
    output = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "output"))
    ).text
    assert "Card:" in output
    assert "Status:" in output


@pytest.mark.skip(reason="Skipping until selenium can launch the application.")
def test_press_socket_testing_buttons(driver):
    # Start browser and navigate to the URL
    time.sleep(2)
    driver.get("http://localhost:5000/blackjack")  # URL where Flask app runs

    # Wait for the hit button to be present
    hit_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "socket-debugger-button-1"))
    )
    hit_button.click()

    # Verify the output
    output = WebDriverWait(driver, 2).until(
        EC.presence_of_element_located((By.ID, "output"))
    ).text
    assert "Card:" in output
    assert "Status:" in output
