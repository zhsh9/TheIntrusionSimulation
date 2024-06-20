import requests
import multiprocessing
import time
from itertools import islice
# Import from the same directory
from base_gen import BaseGen
from dvwa.login import login
from dvwa.user_token import extract_user_token
from dvwa.alter_level import alter_level
from dvwa.sql_injection import sql_injection_request


class DVWA_Base_Gen(BaseGen):
    def __init__(self) -> None:
        super().__init__()
        self.url = 'http://localhost:8000'
        self.description = 'DVWA (Damn Vulnerable Web Application) is a PHP/MySQL web application that is damn vulnerable. Its main goal is to be an aid for security professionals to test their skills and tools in a legal environment, help web developers better understand the processes of securing web applications and aid teachers/students to teach/learn web application security in a classroom environment.'
        self.security = 'impossible'  # Choice: low, medium, high, impossible
        self.cookies = {'PHPSESSID': '8112692f6946472276b6f197d13af8fb', 'security': self.security}
        # DVWA site info
        self.user_token = extract_user_token()  # 4e74b1c5829eeb43ce102a0add65041c
        self.cookies['PHPSESSID'] = self.phpsessionid = login(self.user_token, self.cookies)  # 8112692f6946472276b6f197d13af8fb
        # Generators
        self.p_normal = None
        self.p_exploit = None
        self.p_fuzz = None
    
    def check_status(self):
        """Check the status of DVWA
        """
        resp = requests.get(self.url)
        if resp.status_code == 200:
            return True
        else:
            return False
    
    def config_level(self, level: str):
        """Configure the level level of DVWA
        """
        alter_level(self.cookies, self.user_token, level)
    
    def terminate(self):
        """Terminate the running processes
        """
        if self.p_normal:
            self.p_normal.terminate()
        if self.p_exploit:
            self.p_exploit.terminate()
        if self.p_fuzz:
            self.p_fuzz.terminate()
    
    def normal_generate(self):
        """Periodically generate normal network traffic data
        """
        return super().normal_generate()
    
    def fuzz_generate(self):
        """Periodically generate fuzz network traffic data
        """
        return super().fuzz_generate()
    
    def exploit_generate(self):
        """Periodically generate exploit network traffic data, e.g.
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
        return super().exploit_generate()

    
class DVWA_SQLi_Gen(DVWA_Base_Gen):
    def worker(self, file_path: str):
        with open(file_path, 'r') as file:
            while True:
                lines = list(islice(file, 10000))  # Read 10,000 lines at a time
                if not lines:
                    break  # Exit loop if no more lines to read
                for line in lines:
                    if line: sql_injection_request(
                        self.cookies,
                        self.user_token,
                        line.strip()
                    )
                    time.sleep(1)  # Wait for 1 second before the next request
    
    def normal_generate(self):
        """Periodically generate normal network traffic data
        """
        # Create and start a subprocess
        self.p_normal = multiprocessing.Process(target=self.worker, args=('./dvwa/sqli_normal.txt',))
        self.p_normal.start()
    
    def fuzz_generate(self):
        """Periodically generate fuzz network traffic data
        """
        # Create and start a subprocess
        self.p_fuzz = multiprocessing.Process(target=self.worker, args=('./dvwa/sqli_fuzz.txt',))
        self.p_fuzz.start()
    
    def exploit_generate(self):
        """Periodically generate exploit network traffic data
        """
        # Create and start a subprocess
        self.p_exploit = multiprocessing.Process(target=self.worker, args=('./dvwa/sqli_exp.txt',))
        self.p_exploit.start()        

if __name__ == '__main__':
    dvwa = DVWA_SQLi_Gen()
    print(f"DVWA Status Check: {dvwa.check_status()}")
    print(f"user_token: {dvwa.user_token}, Cookies: {dvwa.cookies}")
    dvwa.config_level('impossible')
    dvwa.fuzz_generate()