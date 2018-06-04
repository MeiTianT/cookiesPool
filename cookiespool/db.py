import random
import redis
from cookiespool.config import *

#实现：将账号信息和cookies保存为两个Hash，Hash名称实现二级分类便于扩展
#实现逻辑：账号由用户名密码组成，可存储为用户名和密码的映射
#cookies存储为用户名和cookies的映射
#建立两个Hash，Hash的Key为账号，Value为密码或Cookies
#实现Hash二级分类：Hash名称可以为accounts:weibo或cookies：weibo,weibo可扩展为其他
#人话：以键值对的形式存储用户名、密码和用户名、cookies，Hash名为accounts:weibo（其他）
class RedisClient(object):
    def __init__(self, type, website, host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD):
        """
        初始化Redis连接
        :param host: 地址
        :param port: 端口
        :param password: 密码
        :param type:类型（account or cookies)
        :param website:站点名称（ex：weibo,zhihu...)
        """
        # 创建StrictRedis对象,与redis服务器建⽴连接，db=1,指定数据库为db1
        self.db = redis.StrictRedis(host=host, port=port, password=password, db=1,decode_responses=True)
        self.type = type
        self.website = website

    def name(self):
        """
        获取Hash的名称
        :return: Hash名称

        {type}:{website}
        Hash名称做二级分类
        accounts：weibo
        cookies:weibo

        可扩展为accounts：zhihu等
        """
        return "{type}:{website}".format(type=self.type, website=self.website)

    def set(self, username, value):
        """
        设置键值对
        :param username: 用户名
        :param value: 密码或Cookies
        :return:
        accounts：weibo（用户名：密码）
        cookies：weibo（用户名：cookies）
        """
        return self.db.hset(self.name(), username, value)

    def get(self, username):
        """
        根据键名获取键值(密码或cookies）
        :param username: 用户名
        :return:
        """
        return self.db.hget(self.name(), username)

    def delete(self, username):
        """
        根据键名删除键值对(密码或cookies）
        :param username: 用户名
        :return: 删除结果
        """
        return self.db.hdel(self.name(), username)

    def count(self):
        """
        获取数目（accounts OR cookies）
        :return: 数目
        """
        return self.db.hlen(self.name())

    def random(self):
        """
        随机得到键值，用于随机Cookies获取
        :return: 随机Cookies
        """
        return random.choice(self.db.hvals(self.name()))

    def usernames(self):
        """
        获取所有账户信息
        :return: 所有用户名
        """
        return self.db.hkeys(self.name())

    def all(self):
        """
        获取所有键值对
        :return: 用户名和密码或Cookies的映射表
        """
        return self.db.hgetall(self.name())


if __name__ == '__main__':
    conn = RedisClient('accounts','weibo')
    result = conn.set('vlnmhswc@sina.cn' ,'tttt55555')
    print(result)