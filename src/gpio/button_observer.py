class ButtonObserver:
    """Observer Pattern — encapsulates a GPIO event listener."""
    def __init__(self, pin: int, callback):
        self.pin = pin
        self.callback = callback
