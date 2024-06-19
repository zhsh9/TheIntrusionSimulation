from abc import ABC, abstractmethod


class HttpServerMonitor(ABC):
    def __init__(self) -> None:
        super().__init__()
        self.monitored_files = set()
    
    @abstractmethod
    def start(self):
        """Start monitoring the HTTP server"""
        pass
    
    @abstractmethod
    def stop(self):
        """Stop monitoring the HTTP server"""
        pass