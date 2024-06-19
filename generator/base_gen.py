from abc import ABC, abstractmethod


class BaseGen(ABC):
    @abstractmethod
    def normal_generate(self):
        """Periodically generate normal network traffic data
           - Visit a webpage in a reasonable human speed with clean data (GET)
           - Submit a form in a reasonable human speed with clean data (POST)
           - etc.
        """
        pass
    
    @abstractmethod
    def fuzz_generate(self):
        """Periodically generate malicious network traffic data (fuzz code), e.g.
           - Brute Force
           - Command Injection
           - CSRF
           - File Inclusion
           - File Upload
           - Insecure CAPTCHA
           - SQL Injection
           - SQL Injection (Blind)
           - XSS (Reflected)
           - XSS (Stored)
        """
        pass
    
    @abstractmethod
    def exploit_generate(self):
        """Periodically generate malicious network traffic data (exploit code), e.g.
           - SQL Injection
           - XSS
           - CSRF
           - DDOS (not recommended for this project)
           - etc.
        """
        pass