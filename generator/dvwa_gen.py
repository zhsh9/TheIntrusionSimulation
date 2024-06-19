from base_gen import BaseGen
import requests
from dvwa.login import login
from dvwa.user_token import extract_user_token
from dvwa.alter_level import alter_level
from dvwa.sql_injection import sql_injection_request


class DVWAGen(BaseGen):
    def __init__(self) -> None:
        super().__init__()
        self.url = 'http://localhost:8000'
        self.description = 'DVWA (Damn Vulnerable Web Application) is a PHP/MySQL web application that is damn vulnerable. Its main goal is to be an aid for security professionals to test their skills and tools in a legal environment, help web developers better understand the processes of securing web applications and aid teachers/students to teach/learn web application security in a classroom environment.'
        self.security = 'impossible'  # Choice: low, medium, high, impossible
        self.cookies = {'PHPSESSID': '8112692f6946472276b6f197d13af8fb', 'security': self.security}
        # DVWA site info
        self.user_token = extract_user_token()  # 4e74b1c5829eeb43ce102a0add65041c
        self.cookies['PHPSESSID'] = self.phpsessionid = login(self.user_token, self.cookies)  # 8112692f6946472276b6f197d13af8fb
    
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
    
    def normal_generate(self):
        """Periodically generate normal network traffic data
        """
        pass
    
    def fuzz_generate(self):
        """Periodically generate malicious network traffic data (fuzz code)
        """
        pass
    
    def exploit_generate(self):
        """Periodically generate malicious network traffic data (exploit code), e.g.
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
        exp = r"1' ORDER BY 3--+"
        resp = sql_injection_request(self.cookies, self.user_token, exp)
        print(f"SQL Injection Response, Status Code: {resp.status_code}")
        

if __name__ == '__main__':
    dvwa = DVWAGen()
    print(f"DVWA Status Check: {dvwa.check_status()}")
    print(f"user_token: {dvwa.user_token}, Cookies: {dvwa.cookies}")
    dvwa.config_level('impossible')
    dvwa.exploit_generate()