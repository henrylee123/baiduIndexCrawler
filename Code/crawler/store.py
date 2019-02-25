'''
批量爬取百度指数的爬虫，配置文件在conf.json里面
更新日期：20181109
更改者：李宗衡
'''
import cx_Oracle
import uuid
from .myLog import Add_Log


@Add_Log(__name__)
class OracleStore():

    def __init__(self, user, password, dsn, *l, **d):
        self.__conn = cx_Oracle.connect(user, password, dsn)
        self.__cur = cx_Oracle.Cursor(self.__conn)


    def store_badu_index(self,insert_sql, kwnm, areanm, date_list, value_list):
        """
        存储百度指数
        :param kwnm: 关键词
        :param areanm: 地区
        :param totalbaiduindex:
        包含这一段时间内的每一个时间点与每一个时间点对应的热搜值
        :return:
        """
        print(value_list)
        self.__cur.prepare(insert_sql)
        crawlerId = uuid.uuid1().hex.upper()
        param = []

        for date_, value in zip(date_list, value_list):
            if value == "":
                value = 0
            elif not isinstance(value,int):
                value = int(value.strip())
            param.append((uuid.uuid1().hex.upper(), crawlerId, areanm,
                          kwnm, date_, value))

        self.__cur.executemany(None, param)
        self.__conn.commit()


    def __store_error_url(self):
        pass