import requests


def login(user_token, cookies) -> str:
    headers = {
        'Host': '127.0.0.1:8000',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        # 'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/x-www-form-urlencoded',
        # 'Content-Length': '56',
        'Origin': 'http://127.0.0.1:8000',
        'Connection': 'close',
        # 'Referer': 'http://127.0.0.1:8000/login.php',
        # 'Upgrade-Insecure-Requests': '1',
        # 'Sec-Fetch-Dest': 'document',
        # 'Sec-Fetch-Mode': 'navigate',
        # 'Sec-Fetch-Site': 'same-origin',
        # 'Sec-Fetch-User': '?1',
        # 'Cookie': 'PHPSESSID=8112692f6946472276b6f197d13af8fb; security=impossible',
    }

    data = {
        'username': 'admin',
        'password': 'password',
        'Login': 'Login',
        'user_token': user_token,
    }

    response = requests.post('http://127.0.0.1:8000/login.php', cookies=cookies, headers=headers, data=data, allow_redirects=False, verify=False)
    # sprint(response)

    # Print the response headers
    # print("Response Headers:")
    # for key, value in response.headers.items():
    #     print(f"{key}: {value}")

    # Extract PHPSESSID from the response cookies
    phpsessid = response.cookies.get('PHPSESSID')
    
    return phpsessid