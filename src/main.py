import time
from core.serial_manager import SerialManager
from output.serial_output import SerialOutput
from core.teletype_controller import TeletypeController

if __name__ == "__main__":
    serial_mgr = None
    teletype = None

    try:
        serial_mgr = SerialManager("/dev/ttyUSB0", 110)
        serial_mgr.connect()
        output = SerialOutput(serial_mgr)
        teletype = TeletypeController(output)

        #Example - Send a file when button on GPIO 18 is pressed
        teletype.add_button(10, teletype.make_file_callback("message.txt"))
        #Example - Send different messages for other buttons
        teletype.add_button(17, teletype.make_text_callback("HELLO FROM BUTTON 1\r\n"))
        teletype.add_button(27, teletype.make_text_callback("STATUS REQUEST\r\n"))
        teletype.add_button(22, teletype.make_text_callback("GOODBYE\r\n"))

        print("Ready. Press Ctrl+C to exit.")
        while True:
            time.sleep(0.1)

    except KeyboardInterrupt:
        print("\nStopping...")
    finally:
        if serial_mgr:
            serial_mgr.disconnect()
        if teletype:
            teletype.cleanup_gpio()
