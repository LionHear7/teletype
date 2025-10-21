# Teletype Raspberry Pi Controller

This project allows you to send text to a vintage teletype device connected to a Raspberry Pi via serial 
port.
You can also control the teletype using physical buttons connected to GPIO pins.

## Features
- Text sanitization (uppercase only, CRLF line endings, tab to spaces)
- Serial output with configurable baudrate and delay
- GPIO button configuration with callback functions
- Modular design for future expansion

## Structure
- `core/`: serial connection and teletype facade
- `output/`: strategies for sending text (serial, console, etc.)
- `gpio/`: pin control
- `teletype_controller.py`: text sanitation and dispatch.
- `main.py`: entry point for execution.

## Requirements
```bash
pip install -r requirements.txt

## Run
```bash
python3 src/main.py

## Collaborations

If you want to collaborate, please drop a request @ riccardo.tonon@gmail.com


