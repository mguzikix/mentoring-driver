import serial
import serial.tools.list_ports


class SerialDriver:
    """
    SerialDriver manages communication over a serial port using a specific USB device (by VID/PID).
    """

    DEFAULT_VID: int = 0x067B
    DEFAULT_PID: int = 0x2303

    def __init__(self, baudrate: int = 115200, timeout: float = 1.0) -> None:
        """
        Initialize the SerialDriver instance.

        Parameters
        ----------
        baudrate : int
            The baud rate for the serial communication.
        timeout : float
            Timeout for read operations in seconds.
        """
        self.vid: int = self.DEFAULT_VID
        self.pid: int = self.DEFAULT_PID
        self.baudrate: int = baudrate
        self.timeout: int = timeout
        self.serial: serial.Serial = None
        self.port: str = self.detect_device()

    @staticmethod
    def detect_device(vid: int = DEFAULT_VID, pid: int = DEFAULT_PID) -> None:
        """
        Detect the serial port of the device with specified VID and PID.

        Parameters
        ----------
        vid : int
            Vendor ID of the device.
        pid : int
            Product ID of the device.

        Returns
        -------
        str or None
            The port name if device is found, otherwise None.
        """
        ports = serial.tools.list_ports.comports()
        for port in ports:
            if port.vid == vid and port.pid == pid:
                print(f"Device found on port: {port.device}")
                return port.device
        print("Device not found.")
        return None

    def open_connection(self) -> None:
        """
        Open the serial connection to the detected port.
        """
        if self.port:
            try:
                self.serial = serial.Serial(
                    port=self.port, baudrate=self.baudrate, timeout=self.timeout
                )
                self.serial.flushInput()
                self.serial.flushOutput()
                print(f"Connection opened on {self.port}")
            except serial.SerialException as e:
                print(f"Error opening serial connection: {e}")
        else:
            print("Cannot open connection. No device port found.")

    def close_connection(self) -> None:
        """
        Close the serial connection if it's open.
        """
        if self.serial and self.serial.is_open:
            self.serial.close()
            print("Serial connection closed.")
        else:
            print("No open connection to close.")

    def __del__(self) -> None:
        """
        Destructor that ensures the serial connection is closed.
        """
        self.close_connection()

    def read_line(self) -> str:
        """
        Read a single line from the serial port.

        Returns
        -------
        str
            The decoded line read from the serial port.
        """
        try:
            resp = self.serial.readline()
            print(f"Response: {resp}")
            return resp.decode('utf-8')
        except serial.SerialTimeoutException as e:
            print("Timeout when waiting for reply")

    def write_message(self, command: str, value: str = "") -> None:
        """
        Write a formatted message to the serial port.

        Parameters
        ----------
        command : str
            The command string to send.
        value : str, optional
            The value to format into the command, by default "".
        """
        out = bytes(command.format(value) + "\r\n", "utf-8")
        print(f"Sending: {out}")
        self.serial.write(out)
