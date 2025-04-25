import pytest
from driver_mguzikix.serial_driver import SerialDriver
import serial


@pytest.fixture(scope="module")
def serial_connection():
    """
    Fixture to create and manage a serial connection for tests.
    """
    driver = SerialDriver()
    try:
        driver.open_connection()
    except serial.SerialException as e:
        pytest.fail(f"Error opening connection: {e}")

    yield driver
    driver.close_connection()
