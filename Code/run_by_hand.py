from  auto_run import BaiduIndexSpider
from setting import conf, run_date


if __name__ == "__main__":
    bdis = BaiduIndexSpider(
                start_date=run_date["start_date"],
                end_date=run_date["end_date"], **conf)
