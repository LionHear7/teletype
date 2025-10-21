import RPi.GPIO as GPIO
from gpio.button_observer import ButtonObserver

class TeletypeController:
    """Facade — coordinates GPIO, serial communication, and text handling."""

    def __init__(self, output_strategy):
        self.output = output_strategy
        self.gpio_initialized = False
        self.observers = []

    @staticmethod
    def sanitize_text(text: str) -> str:
        text = text.upper().replace('\t', ' ' * 4)
        text = text.replace('\r\n', '\n').replace('\r', '\n').replace('\n', '\r\n')
        return ''.join(c if c in ('\r', '\n') or 32 <= ord(c) <= 126 else ' ' for c in text)

    @staticmethod
    def read_file(path: str) -> str:
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            return f.read()

    def setup_gpio(self):
        if not self.gpio_initialized:
            GPIO.setmode(GPIO.BCM)
            self.gpio_initialized = True
            print("GPIO initialized (BCM mode).")

    def add_button(self, pin: int, callback, pull="down", edge="RISING", bounce_ms=200):
        self.setup_gpio()
        pull_cfg = GPIO.PUD_DOWN if pull == "down" else GPIO.PUD_UP
        GPIO.setup(pin, GPIO.IN, pull_up_down=pull_cfg)
        edge_type = getattr(GPIO, edge.upper())
        GPIO.add_event_detect(pin, edge_type, callback=callback, bouncetime=bounce_ms)
        self.observers.append(ButtonObserver(pin, callback))
        print(f"Button on GPIO {pin} registered ({edge}, pull={pull})")

    def cleanup_gpio(self):
        GPIO.cleanup()
        print("GPIO cleaned up.")

    def send_text(self, text: str):
        self.output.send(self.sanitize_text(text))

    def make_text_callback(self, message: str):
        """Factory that returns a GPIO callback tied to a specific text message."""
        def callback(channel):
            print(f"[GPIO {channel}] -> SEND MESSAGE: {message.strip()}")
            self.send_text(message)
        return callback

    def send_from_file(self, file_path: str):
        self.send_text(self.read_file(file_path))

    def make_file_callback(self, file_path: str):
        """Factory that returns a GPIO callback tied to a specific file."""
        def callback(channel):
            print(f"[GPIO {channel}] -> FILE SEND ({file_path})")
            self.send_from_file(file_path)
        return callback

