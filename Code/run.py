'''
批量爬取百度指数的爬虫，配置文件在conf.json里面
更新日期：20181109
更改者：李宗衡
'''
from crawler.myDate import MyDateTime
from setting import download_days
import sys
from crawler.singleAreaCral import Login, SingleAreaCral
from crawler.store import OracleStore
import json


class BaiduIndexSpider():
    def __init__(self,
            # 爬取日期列表， 地区代码字典, 百度指数插入语句
            run_date_list, area_code, insert_sql, missing_date_json_path,
             # cral 参数
             url, get_decode_key_url, headers, decode_js,
                 timeout, word_list_split_len, key_word_list,
             # login 参数
             user, psw, chrome_driver_path, login_url,
             # store 参数
             conn):
        self.missing_date_json_path = missing_date_json_path
        with open(missing_date_json_path, "rb") as f:
            json_ = f.read()
            d = json.loads(json_)
            self.missing_date_list = d.get("missing_date", [])
        self.run_date_list = run_date_list
        self.area_code= area_code
        self.insert_sql = insert_sql
        # 下面分别为：单地点爬取，登录，存储模块
        self.single_area_cral = SingleAreaCral(url, get_decode_key_url, headers, decode_js,
                             timeout, word_list_split_len, key_word_list)
        self.login = Login(user, psw, chrome_driver_path, login_url)
        self.store = OracleStore(conn)
        super().__init__()


    def start_cral(self):
        self.single_area_cral.cookie = 'BDUSS=mdXR3hiLVk1S0tQY2FmeDNFSlRxMllablRvYWFtZnZaSWthUlpJRX51ajc1cFpjQVFBQUFBJCQAAAAAAAAAAAEAAABW71JAwO7X2rriMgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAPtZb1z7WW9cV'
        # self.single_area_cral.cookie = "BDUSS=" + self.login.get_cookie()
        # 循环输入地区，获取baiduIndex值
        for area_en, area_code in  self.area_code.items():
            start_date = self.run_date_list[0]
            end_date = self.run_date_list[-1]
            # 如果有missing date 加到前面
            if self.missing_date_list:
                start_date = self.missing_date_list[0]
            # 开始请求
            self.is_first = 1
            for key_word, store_data in self.single_area_cral.get_data(
                                    area_code, start_date, end_date):
                # 存储的时间（self.run_date_list 是请求的时间，存储时间会缺失几个时间点）
                true_time_list = MyDateTime.get_date_during(
                    self.single_area_cral.true_start_date,
                    self.single_area_cral.true_end_date)
                # 缺失的日期存起来
                self.store_lost_date(self.is_first, self.single_area_cral.true_end_date, end_date)
                # 存储
                self.store.store_badu_index(self.insert_sql, key_word,
                    area_en, true_time_list, store_data)


    def  store_lost_date(self, is_first, start_date, end_date):
        # 缺失的日期存起来(百度指数日期是同步的)
        if is_first == 1:
            missing_date_list = MyDateTime.get_date_during(
                start_date, end_date)[1: -1]

            with open(self.missing_date_json_path, "w") as f:
                d = {"missing_date": missing_date_list}
                j = json.dumps(d)
                f.write(j)
            self.is_first = 0

def check_run_date():
    mydt = MyDateTime()
    run_date_list = mydt.get_run_date(download_days)
    if not run_date_list:
        sys.exit(0)
    return run_date_list


from setting import conf


if __name__ == "__main__":
    run_date_list = check_run_date()
    baidu_spider = BaiduIndexSpider(run_date_list=run_date_list, **conf)
    baidu_spider.start_cral()