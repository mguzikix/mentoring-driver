import pytest
from driver_mguzikix.serial_driver import SerialDriver
import time

def test_read_entire_serial_sequence(serial_connection):
    """
    Test reads a sequence of operations from the serial connection 
    and verifies if the data matches the expected responses.

    Parameters
    ----------
    serial_connection : SerialDriver
        The SerialDriver instance, provided by the fixture.
    """

    start_time = time.time()
    max_wait_time = 15
    response = []  
    expected_response = [
        'Operation 0\r\n', 'Operation 1\r\n', 'Operation 2\r\n', 'Operation 3\r\n', 
        'Operation 4\r\n', 'Operation 5\r\n', 'Operation 6\r\n', 'Operation 7\r\n', 
        'Operation 8\r\n', 'Operation 9\r\n', 'Operation 10\r\n', 'ALL DONE!\r\n'
    ]  
    line = "" 
    while "ALL DONE!" not in line:
        line = serial_connection.read_line()
        
        if time.time() - start_time > max_wait_time:
            pytest.fail("Didn't receive the 'ALL DONE!' message within the wait time.")
        time.sleep(1)

    for i in range(len(expected_response)): 
        line = serial_connection.read_line()  
        response.append(line) 
        time.sleep(1)

    assert response == expected_response, f"Expected: {expected_response}, but got: {response}"

def test_send_message(serial_connection):
    """
    Test sends two messages ('A' and 'B') via serial, waits for a response, 
    and checks if they match the expected values.

    Parameters
    ----------
    serial_connection : SerialDriver
        The SerialDriver instance, provided by the fixture.
    """
    response_a = []
    response_b = []
    expected_response= ['DATA RECEIVED!\r\n', 'ACTION RECEIVED!\r\n']
 
    serial_connection.serial.reset_input_buffer()

    serial_connection.write_message('A')
    time.sleep(0.5)
    for i in range(2):
        response_a.append(serial_connection.read_line())

    assert response_a == expected_response , f"Expected {expected_response}, but got: {response_a}"

    serial_connection.write_message('B')
    time.sleep(1)
    for i in range(2):
        response_b.append(serial_connection.read_line())

    assert expected_response[0] in response_b, "'DATA RECEIVED!' not found in response after 'B'"
    assert expected_response[1] not in response_b, "'ACTION RECEIVED!' should not be in response after 'B'"