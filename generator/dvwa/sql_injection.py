import requests
from urllib.parse import urlencode


def sql_injection_request(cookies, user_token, id):
    base_url = r'http://127.0.0.1:8000/vulnerabilities/sqli/'
    headers = {
        'Host': '127.0.0.1:8000',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        # 'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'close',
        'Referer': base_url,
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        # 'Cookie': 'PHPSESSID=d54eb5e8bce5e2aacdab3f780235b90a; security=impossible',
    }

    params = {
        'id': str(id),
        'Submit': 'Submit',
        'user_token': user_token,
    }

    response = requests.get(
        base_url,
        params=params,
        cookies=cookies,
        headers=headers,
        verify=False,
    )
    
    full_url = f"{base_url}?{urlencode(params)}"
    print(f"Request URL: {full_url}")
    
    return response