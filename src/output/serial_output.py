import time
from .output_strategy import OutputStrategy
from core.serial_manager import SerialManager

class SerialOutput(OutputStrategy):
    """Concrete Strategy for serial output."""

    def __init__(self, serial_manager: SerialManager, delay: float = 0.02):
        self.serial_manager = serial_manager
        self.delay = delay

    def send(self, text: str):
        for ch in text:
            self.serial_manager.write(ch)
            time.sleep(self.delay)
