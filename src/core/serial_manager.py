import serial
import os

class SerialManager:
    """Singleton Pattern — ensures only one serial connection exists."""
    _instance = None

    def __new__(cls, port="/dev/ttyUSB0", baudrate=110):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.port = port
            cls._instance.baudrate = baudrate
            cls._instance.serial = None
            cls._instance.available = False
        return cls._instance

    def connect(self):
        if self.serial is None or getattr(self.serial, "is_open", False):
            if not os.path.exists(self.port):
                print(f"Serial port {self.port} not found. Continuing without serial.")
                self.available = False
                return

            try:
                self.serial = serial.Serial(
                    port=self.port,
                    baudrate=self.baudrate,
                    bytesize=serial.EIGHTBITS,    # cs8
                    parity=serial.PARITY_NONE,    # -parenb
                    stopbits=serial.STOPBITS_ONE, # -cstopb
                    xonxoff=False,                 # -ixon -ixoff
                    rtscts=False,                  # -crtscts
                    timeout=1
                )
                self.available = True
                print(f"Serial connected on {self.port} ({self.baudrate} baud).")

            except serial.SerialException as e:
                print(f"Serial connection failed: {e}")
                self.available = False


    def disconnect(self):
        if self.serial and getattr(self.serial, "is_open", False):
            self.serial.close()
            print("Serial disconnected.")
            self.serial = None
            self.available = False

    def write(self, text: str):
        if not self.available or not self.serial:
            # Graceful fallback — do nothing if serial unavailable
            print(f"(Serial unavailable) → {text.strip()}")
            return
        self.serial.write(text.encode('ascii', errors='ignore'))
        self.serial.flush()
