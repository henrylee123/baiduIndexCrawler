'''
批量爬取百度指数的爬虫，配置文件在conf.json里面
更新日期：20181109
更改者：李宗衡
ATTENTION！！
-----------------
如果登录出现验证码会报错，请按照以下三种解决方法：
-----------------
ATTENTION！！
'''
# auto run  自动运行
download_days = [10, 25]

#run by hand 手动运行
run_date = {
    "start_date": "2018-10-01",
    "end_date": "2019-2-25"
}

# 日志conf
log_conf = {
    "level": "DEBUG",
    "filename": "output.log",
    "datefmt": "%Y/%m/%d %H:%M:%S",
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(lineno)d - %(module)s - %(message)s"
}

# crawler conf
conf = {
    "missing_date_json_path": "missing_date.json",
    "area_code": {
        "guangzhou": "95", "shenzhen": "94", "foshan": "196",
         "huizhou": "199", "shantou": "212", "dongguan": "133",
         "maoming": "203", "jiangmen": "198", "zhuhai": "200",
         "zhanjiang": "197", "zhaoqing": "209", "jieyang": "205",
         "zhongshan": "207", "shaoguan": "201", "yangjiang": "202",
         "yunfu": "195", "meizhou": "211", "qingyuan": "208",
         "chaozhou": "204", "shanwei": "213", "heyuan": "210",
         "hangzhou": "138", "wenzhou": "149", "ningbo": "289",
         "jinhua": "135", "taizhou": "287", "jiaxing": "304",
         "shaoxing": "303", "huzhou": "305", "lishui": "134",
         "quzhou": "288", "zhoushan": "306"
    },

    # cral setting
    "url": "http://index.baidu.com/api/SearchApi/index",
    "get_decode_key_url": "http://index.baidu.com/Interface/api/ptbk?uniqid=",
    "timeout": 15,
    "headers": {
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Connection": "keep-alive",
        #  你的cookie，必须加
        "Cookie": "",
        "Host": "index.baidu.com",
        "Referer": "http://index.baidu.com/v2/main/index.html",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
    },
    "decode_js": """
            function decrypt(uniqid_ptbk, index_data) {
            for (var a = uniqid_ptbk.split(""), i = index_data.split(""), n = {}, s = [], o = 0; o < a.length / 2; o++)
                n[a[o]] = a[a.length / 2 + o];
            for (var r = 0; r < index_data.length; r++)
                s.push(n[i[r]]);
            return s.join("")
            }
            """,
    # 一次请求发送都少个关键词
    "word_list_split_len": 5,
    "key_word_list": ["登革热", "登革热症状", "登革热病", "登革热病毒", "登革热病例", "发烧"],


    # login setting
    "user": "15622108121",
    "psw": "zhangheng2",
    "chrome_driver_path": "C:/Users/Admin/Desktop/chromedriver.exe",
    "login_url": "https://index.baidu.com/",


    # Oracle conn info
    "conn": {
        "table_name": "BDIDXINDEXES",
        "db_type": "oracle+cx_oracle",
        "user": "hiibase",
        "password": "hiibase",
        "dsn": "200.100.100.69:1521/dgr"
    },
    "insert_sql": "insert into BDIDXINDEXES(FIDXID,FCRAWLID,FAREANM,FKEYWORD,FIDXDTKEY,FIDXVAL) values (:1,:2,:3,:4,:5,:6)"
}