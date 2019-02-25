"""
批量爬取百度指数的爬虫，配置文件在conf.json里面
更新日期：20181109
更改者：李宗衡
ATTENTION！！
-----------------
如果登录出现验证码会报错，请按照以下三种解决方法：
（1）在config.json更换别的用户密码
（2）在baidudu1.py中login函数中# 
（3）编写一个验证码识别模块
-----------------
ATTENTION！！
"""
# 加载系统模块
import requests
import time
import js2py
from selenium import webdriver
from crawler.myLog import Add_Log
from .myDate import MyDateTime


@Add_Log(__name__)
class Login():
    def __init__(self, user, psw, chrome_driver_path, login_url):
        self.__user = user
        self.__psw = psw
        self.chrome_driver_path =chrome_driver_path
        self.login_url = login_url


    def get_cookie(self):
        # open chromedriver & requests
        self.c = webdriver.Chrome(self.chrome_driver_path)
        self.c.get(self.login_url)
        time.sleep(3)
        # input user pwd and update
        self.__login()
        # get cookie
        cookie = self.c.get_cookie('BDUSS')["value"]
        # close chromedriver
        self.c.close()
        self.c.quit()
        return cookie

    def __login(self):
        self.c.find_element_by_xpath('//*[@id="home"]/div[1]/div[2]/div[1]/div[5]/span/span').click()
        time.sleep(5)
        self.c.find_element_by_xpath('//*[@id="TANGRAM__PSP_4__userName"]').send_keys(self.__user)
        time.sleep(1)
        self.c.find_element_by_xpath('//*[@id="TANGRAM__PSP_4__password"]').send_keys(self.__psw)
        time.sleep(1)
        self.c.find_element_by_xpath('//*[@id="TANGRAM__PSP_4__submit"]').click()
        time.sleep(3)
        n=14
        while True:
            try:
                self.c.find_element_by_xpath('//*[@id="home"]/div[1]/div[2]/div[1]/div[4]/span/span')
            except Exception:
                break
            try:
                m = str(n)
                self.c.find_element_by_xpath('//*[@id="TANGRAM__{m}__header_a"]'.format(m=m)).click()
                time.sleep(2)
                self.c.find_element_by_xpath('//*[@id="TANGRAM__PSP_4__submit"]').click()
                time.sleep(3)
                n += 1
            except Exception:
                # todo 断点处（验证码手动输入）
                self.c.find_element_by_xpath('// *[ @ id = "search-input-form"] / input[3]').send_keys('haha')
                time.sleep(1)
                self.c.find_element_by_xpath('//*[@id="home"]/div[2]/div[2]/div/div[1]/div/div[2]/div/span/span').click()


@Add_Log(__name__)
class SingleAreaCral():
    """
    每一次循环抛出一个词全时段的已解密热搜值
    get_data: main function
    __decode_data: 解密函数
    __get_decode_key: 获取秘钥
    """
    def __init__(self, url, get_decode_key_url, headers, decode_js,
                 timeout, word_list_split_len, key_word_list):
        self.__url = url
        self.__decode_data_py = js2py.eval_js(decode_js)
        self.__headers = headers
        self.__get_decode_key_url = get_decode_key_url
        self.__timeout = timeout
        self.__word_list_split_len = word_list_split_len
        self.__key_word_list = key_word_list
        self.cookie = None


    def get_data(self, area, start_date, end_date):
        """
        请求百度指数,获取加密数据
        """
        self.__headers["Cookie"] = self.cookie
        for key_word_str in self.__split_N_keyword_list_iterator():
            params = {
                "area": int(area),  # 城市编号 全国 是0,
                "word": key_word_str,  # 关键字
                "startDate": start_date,  # 开始时间  这个列表的值 就是从这个开始时间 到结束时间的
                "endDate": end_date,  # 结束时间  要加上一天
            }

            # 获得5个词全时段的加密热搜值
            index_data = SingleAreaCral.__get_json_data(self.__url, headers=self.__headers, params=params, timeout=self.__timeout)
            self.true_start_date = index_data['userIndexes'][0]["all"]["startDate"]
            self.true_end_date = index_data['userIndexes'][0]["all"]["endDate"]
            # 每一次循环抛出一个词全时段的已解密热搜值  PC+移动端的值
            yield from self.__decode_data(index_data, self.__word_list_split_len)


    def __split_N_keyword_list_iterator(self):
        """
        按顺序5个5个地选择列表中的关键词，并用逗号连在一起后抛出。
        :param key_word_list:
        :return:
        """
        for num in range(int(len(self.__key_word_list)/self.__word_list_split_len) + 1):
            cut_left = num * self.__word_list_split_len
            cut_right = cut_left + self.__word_list_split_len
            tmp_list = self.__key_word_list[cut_left: cut_right]
            yield ','.join(tmp_list)

    def __decode_data(self, index_data, word_list_len=5):
        """
        每一次循环抛出一个词全时段的已解密热搜值
        """
        for idx in range(word_list_len):
            try:
                single_word_index_data = index_data['userIndexes'][idx]["all"]['data']
            except IndexError:
                break
            key_word = index_data['userIndexes'][idx]["word"]
            # 想单独获取pc或wise请将all 改成wise 或pc
            # uniqid_ptbk  为秘钥
            uniqid_ptbk = index_data['uniqid']  # PC+移动端的值
            time.sleep(1)
            # 请求获得解密的密码
            uniqid_ptbk = self.__get_decode_key(uniqid_ptbk)
            # 用密码解密数据
            if single_word_index_data:
                data = self.__decode_data_py(uniqid_ptbk, single_word_index_data)  # 获取解密函数
                yield key_word, data.split(",")
            else:  # 没有数据会返回''
                time_list = MyDateTime.get_date_during(
                    self.true_start_date, self.true_end_date)
                data = [0] * len(time_list)
                yield key_word, data


    def __get_decode_key(self, uniqid_ptbk):
        """
        获取解密数据与密码的生成码
        拿uniqid_ptbk 参数（密码生成码）请求得到 密码
        """
        url = self.__get_decode_key_url + str(uniqid_ptbk)
        return SingleAreaCral.__get_json_data(url, headers=self.__headers, timeout=self.__timeout)


    @classmethod
    def __get_json_data(cls, url, *args, **kwargs):
        response = requests.get(url, *args, **kwargs)
        # cookie 要加上 BDUSS
        data = response.text
        data = eval(data)
        return data["data"]