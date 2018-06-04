import json
import requests
from requests.exceptions import ConnectionError
from cookiespool.db import *

#实现：检测并移除失效cookies
#逻辑：遍历池中所有cookies，设置对应检测链接，
# 用cookies去请求链接，如果请求成功则有效，否则为无效cookies，移除。
#移除cookies后，生成器重新生成该cookies
class ValidTester(object):
    def __init__(self, website='default'):
        self.website = website
        self.cookies_db = RedisClient('cookies', self.website)
        self.accounts_db = RedisClient('accounts', self.website)

    def test(self, username, cookies):
        raise NotImplementedError

    def run(self):
        cookies_groups = self.cookies_db.all()
        for username, cookies in cookies_groups.items():
            self.test(username, cookies)


class WeiboValidTester(ValidTester):
    def __init__(self, website='weibo'):
        ValidTester.__init__(self, website)

    def test(self, username, cookies):
        print('正在测试Cookies', '用户名', username)
        try:
            #将cookies转化为字典
            cookies = json.loads(cookies)
        except TypeError:
            print('Cookies不合法', username)
            #格式不正确则删除
            self.cookies_db.delete(username)
            print('删除Cookies', username)
            return
        try:
            test_url = TEST_URL_MAP[self.website]
            #禁止重定向
            response = requests.get(test_url, cookies=cookies, timeout=5, allow_redirects=False)
            if response.status_code == 200:
                print('Cookies有效', username)
            else:
                print(response.status_code, response.headers)
                print('Cookies失效', username)
                self.cookies_db.delete(username)
                print('删除Cookies', username)
        except ConnectionError as e:
            print('发生异常', e.args)

if __name__ == '__main__':
    WeiboValidTester().run()