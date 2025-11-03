import RPi.GPIO as GPIO
import time

# --- CONFIGURE PINS ---
PINS = [4, 5, 12, 13, 16, 17, 18, 20, 21, 22, 23, 24, 25, 26, 27]  # List of BCM pins to test
PULL = GPIO.PUD_DOWN      # Use PUD_UP if buttons are connected to 3.3V

GPIO.setmode(GPIO.BCM)

# Initialize all pins as input with pull-up/down, ignore errors
active_pins = []
for pin in PINS:
    try:
        GPIO.setup(pin, GPIO.IN, pull_up_down=PULL)
        active_pins.append(pin)
    except Exception as e:
        print(f"Failed to setup GPIO {pin}: {e}")

print(f"Testing GPIO pins {active_pins}. Press Ctrl+C to stop.\n")

try:
    while True:
        # Read all active pins
        states = {pin: GPIO.input(pin) for pin in active_pins}
        # Build a status string
        state_str = " | ".join(f"{pin}: {val}" for pin, val in states.items())
        print(state_str, end="\r", flush=True)
        time.sleep(0.2)  # Update every 200ms
except KeyboardInterrupt:
    print("\nStopped by user.")
finally:
    GPIO.cleanup()