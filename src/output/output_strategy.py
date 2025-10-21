from abc import ABC, abstractmethod

class OutputStrategy(ABC):
    """Strategy Pattern — defines a generic interface for text output."""
    @abstractmethod
    def send(self, text: str):
        pass
