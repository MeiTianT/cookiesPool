import requests

from cookiespool.db import RedisClient

#录入账号密码并存储到数据库
#先生成accounts:weibo

conn = RedisClient('accounts', 'weibo')

def set(account, sep=','):
    #逗号作为账号密码的分隔
    username, password = account.split(sep)
    result = conn.set(username, password)
    print('账号', username, '密码', password)
    print('录入成功' if result else '录入失败')


def scan():
    print('请输入账号密码组, 输入exit退出读入')
    while True:
        account = input()
        if account == 'exit':
            break
        set(account)


if __name__ == '__main__':
    scan()