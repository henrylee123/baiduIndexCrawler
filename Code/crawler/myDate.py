import datetime
from .myLog import Add_Log


@Add_Log(__name__)
class MyDateTime():
    def __init__(self):
        self.__today = datetime.date.today()

    def get_run_date(self, download_days):
        today = self.__today.strftime('%Y-%m-%d')
        month = self.__today.month
        year = self.__today.year
        run_date_list = [self.__get_date_of_month(download_day, month, year) for download_day in download_days]
        if today in run_date_list:
            idx = run_date_list.index(today)
            # 调整月与年的值
            if idx == 0:
                if month == 1:
                    year -= 1
                    month = 12
                else: month -= 1
            # 获取起始时间
            start_date = self.__get_date_of_month(download_days[idx  - 1], month, year)
            # 返回所有日期节点
            return start_date, today
        else: return None, None

    def __get_date_of_month(self, day_num, month_num, year_num):
        if day_num > 0:
            return  datetime.date(
                year_num, month_num , day_num).strftime('%Y-%m-%d')
        elif day_num < 0:
            last_date = datetime.date(self.__today.year, self.__today.month + 1, 1) \
                        - datetime.timedelta(1 - day_num)
            return last_date.strftime('%Y-%m-%d')

    @classmethod
    def get_date_during(cls, start_date, end_date):
        """
        返回start_date与end_date段内所有的日期时间 格式：2018-01-01
        不包含结束日期
        :param start_date: 2018-01-01
        :param end_date: 2018-01-31
        """
        date_list = []
        date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d')
        while date <= end_date:
            date_list.append(date.strftime('%Y-%m-%d'))
            date = date + datetime.timedelta(1)
        return date_list