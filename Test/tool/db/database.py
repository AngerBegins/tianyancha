import redis
import pymongo
from DBUtils.PooledDB import PooledDB
import pymysql
import logging
redis_config ={
    'host': '192.168.10.115',
    'port': 6379

}
mysql ={
    'host':'localhost',
    'user':'root',
    'passwd':'123456',
    'db':'tianyancha',
    'port':3306,
    "charset": 'utf8'

}
logger = logging.getLogger('db')
class redisPool:
    def __init__(self):
        self.redis_clint = redis.ConnectionPool(**redis_config)
class mysqlPool(object):

    def __init__(self):
        self.pool = PooledDB(creator=pymysql,
                             mincached=3,
                             maxcached=20,
                             maxconnections=20,
                             host=mysql['host'],
                             user=mysql['user'],
                             passwd=mysql['passwd'],
                             db=mysql['db'],
                             port=mysql['port'],
                             charset=mysql['charset'],)

    def get_conn(self):
        self.conn = self.pool.connection()
        return self.conn

    def close(self,conn):
        conn.close()

    def insert(self,sql):
        conn = self.get_conn()
        cur = conn.cursor()
        result = True
        try:
            cur.execute(sql)
            conn.commit()
        except:
            result = False
            logger.error('入库失败')
        finally:
            conn.rollback()
            cur.close()
            self.close(conn)
            cur.close()
            return result

    def get_data(self,sql):
        list = []
        conn = self.get_conn()
        try:
            cur = conn.cursor()
            cur.execute(sql)
            list = cur.fetchall()
            conn.commit()
            cur.close()
        except:
            result = False
            print('入库失败')
        finally:
            self.close(conn)
            return list


class mongodb(object):
    def __init__(self):
        self.client = pymongo.MongoClient('192.168.10.115', 27017)
        self.db = self.client.tianyancha

    def insert(self, dict):
        collect = self.db.company
        result = False
        try:
            result = collect.insert(dict)
        except:
            logger.error('%s:mogodb入库失败' % dict)
        return result

mongo = mongodb()
# mysql = mysqlPool()
if __name__ == '__main__':
    #申请资源
    pool = mysqlPool()

    # sql = 'insert into company VALUES ("{}","{}","{}")'
    # sql = sql.format('2314579547', '沈阳市人民政府国有资产监督管理委员会','https://www.tianyancha.com/company/2314579547')
    # print(sql)
    # res = pool.insert(sql)
    # sql = 'select * from company'
    # data = pool.get_data(sql)
    # for i in data:
    #     print(i[0],i[1],i[2])
    # print(data)
    dict = {'_id':'1084081696','name':'广州中油洁能燃气连锁有限公司石榴岗经营部', 'url':'https://www.tianyancha.com/company/1084081696'}
    m = mongodb()
    t = m.insert(dict)
    print(t)

