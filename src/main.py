import time
from core.serial_manager import SerialManager
from output.serial_output import SerialOutput
from core.teletype_controller import TeletypeController

from output.console_output import ConsoleOutput

if __name__ == "__main__":
    serial_mgr = None
    teletype = None

    try:
        serial_mgr = SerialManager("/dev/ttyUSB0", 110)
        serial_mgr.connect()
        output = SerialOutput(serial_mgr)
        teletype = TeletypeController(output)

        console_output = ConsoleOutput()

        #Example - Send a file to teletype when button on GPIO 17 is pressed
        teletype.add_button(17, teletype.make_file_callback("message.txt"))

        #Example - Send fixed message to teletype when buttons on GPIO 22 is pressed
        teletype.add_button(22, teletype.make_text_callback("GOODBYE\r\n"))

        #Example - Send a fixed message to console when button on GPIO 27 is pressed
        teletype.add_button(27, lambda pin=None, *args, **kwargs: console_output.send("HELLO FROM BUTTON 27\r\n"))
        
        #Example - Send different messages for other buttons
        #uncomment to use
        # teletype.add_button(17, teletype.make_file_callback("message.txt"))  
        # teletype.add_button(22, teletype.make_text_callback("HELLO FROM BUTTON 22\r\n"))
        # teletype.add_button(27, teletype.make_text_callback("GOODBYE\r\n"))

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
