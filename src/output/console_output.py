from .output_strategy import OutputStrategy

class ConsoleOutput(OutputStrategy):
    """Concrete Strategy for debugging output."""
    def send(self, text: str):
        print(text, end='', flush=True)
