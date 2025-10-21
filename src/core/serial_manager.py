import serial

class SerialManager:
    """Singleton Pattern — ensures only one serial connection exists."""
    _instance = None

    def __new__(cls, port="/dev/ttyUSB0", baudrate=110):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.port = port
            cls._instance.baudrate = baudrate
            cls._instance.serial = None
        return cls._instance

    def connect(self):
        if self.serial is None or not self.serial.is_open:
            self.serial = serial.Serial(
                port=self.port,
                baudrate=self.baudrate,
                bytesize=serial.EIGHTBITS,   # cs8
                parity=serial.PARITY_NONE,   # -parenb
                stopbits=serial.STOPBITS_ONE, # -cstopb
                xonxoff=False,                # -ixon -ixoff
                rtscts=False,                 # -crtscts (opzionale)
                timeout=1
            )
            print(f"Serial connected on {self.port} ({self.baudrate} baud).")

    def disconnect(self):
        if self.serial and self.serial.is_open:
            self.serial.close()
            print("Serial disconnected.")
            self.serial = None

    def write(self, text: str):
        if not self.serial:
            raise RuntimeError("Serial not connected.")
        self.serial.write(text.encode('ascii', errors='ignore'))
        self.serial.flush()
