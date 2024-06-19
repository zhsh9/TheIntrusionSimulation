import requests


def alter_level(cookies, user_token, level):
    headers = {
        'Host': '127.0.0.1:8000',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        # 'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/x-www-form-urlencoded',
        # 'Content-Length': '77',
        'Origin': 'http://127.0.0.1:8000',
        'Connection': 'close',
        'Referer': 'http://127.0.0.1:8000/security.php',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        # 'Cookie': 'PHPSESSID=1f913547813995a657325d1d6f796132; security=high',
    }

    data = {
        'security': level,
        'seclev_submit': 'Submit',
        'user_token': user_token,
    }

    response = requests.post('http://127.0.0.1:8000/security.php', cookies=cookies, headers=headers, data=data, verify=False)

    return response