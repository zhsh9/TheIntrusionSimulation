import requests
from bs4 import BeautifulSoup


def extract_user_token(base_url='http://127.0.0.1:8000') -> str:
    # 创建一个会话对象
    session = requests.Session()

    # 访问登录页面以获取 `user_token`
    login_page_url = base_url + '/login.php'
    login_page_response = session.get(login_page_url, verify=False)

    # 解析页面内容以提取 `user_token`
    soup = BeautifulSoup(login_page_response.text, 'html.parser')
    user_token = soup.find('input', {'name': 'user_token'})['value']

    # 打印获取到的 `user_token`
    # print(f"Extracted user_token: {user_token}")
    
    return user_token