import os
import sys
import pytest
from unittest.mock import patch, MagicMock
from driver_mguzikix.serial_driver import SerialDriver

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "./../src")))


@pytest.fixture
def mock_serial():
    with patch("driver_mguzikix.serial_driver.serial") as mock_serial_class:
        yield mock_serial_class


@pytest.fixture
def mock_list_ports():
    with patch(
        "driver_mguzikix.serial_driver.serial.tools.list_ports.comports"
    ) as mock_comports:
        yield mock_comports


def test_detect_device_found(mock_list_ports):
    mock_port = MagicMock()
    mock_port.vid = 0x067B
    mock_port.pid = 0x2303
    mock_port.device = "COM3"
    mock_list_ports.return_value = [mock_port]

    driver = SerialDriver()
    assert driver.port == "COM3"


def test_detect_device_not_found(mock_list_ports):
    mock_list_ports.return_value = []

    driver = SerialDriver()
    assert driver.port is None


def test_open_connection_success(mock_serial, mock_list_ports):
    # Mocking the device detection
    mock_port = MagicMock()
    mock_port.vid = 0x067B
    mock_port.pid = 0x2303
    mock_port.device = "COM3"
    mock_list_ports.return_value = [mock_port]

    mock_serial_instance = MagicMock()
    mock_serial.Serial.return_value = mock_serial_instance

    driver = SerialDriver()
    driver.open_connection()

    mock_serial.Serial.assert_called_once_with(
        port="COM3", baudrate=115200, timeout=1.0
    )

    mock_serial_instance.flushInput.assert_called_once()
    mock_serial_instance.flushOutput.assert_called_once()


def test_open_connection_no_device(mock_serial, mock_list_ports):
    mock_list_ports.return_value = []

    driver = SerialDriver()
    driver.open_connection()

    mock_serial.assert_not_called()


def test_close_connection(mock_serial):
    # Mocking a successful serial connection
    mock_serial_instance = MagicMock()
    mock_serial_instance.is_open = True
    mock_serial.return_value = mock_serial_instance

    driver = SerialDriver()
    driver.serial = mock_serial_instance
    driver.close_connection()

    mock_serial_instance.close.assert_called_once()


def test_close_connection_no_open_connection(mock_serial):
    # Mocking no open connection
    mock_serial_instance = MagicMock()
    mock_serial_instance.is_open = False
    mock_serial.return_value = mock_serial_instance

    driver = SerialDriver()
    driver.serial = mock_serial_instance
    driver.close_connection()

    mock_serial_instance.close.assert_not_called()


def test_read_line(mock_serial):
    # Mocking a serial instance's readline method
    mock_serial_instance = MagicMock()
    mock_serial_instance.readline.return_value = b"Test response\r\n"
    mock_serial.return_value = mock_serial_instance

    driver = SerialDriver()
    driver.serial = mock_serial_instance
    response = driver.read_line()

    assert response == "Test response\r\n"


def test_write_message(mock_serial):
    # Mocking serial write
    mock_serial_instance = MagicMock()
    mock_serial.Serial.return_value = mock_serial_instance

    driver = SerialDriver()
    driver.serial = mock_serial_instance

    driver.write_message("Hello")
    mock_serial_instance.write.assert_called_once_with(b"Hello\r\n")
