from  run import BaiduIndexSpider
from setting import conf, log_conf
from crawler.myLog import MyLoger
from run import check_run_date
from setting import download_days


def create_table():
    from sqlalchemy.ext.declarative import declarative_base
    import sqlalchemy as sa
    from sqlalchemy import create_engine

    Base = declarative_base()
    conn = "oracle+cx_oracle://hiibase:hiibase@localhost:1521/dgr"
    engine = create_engine(conn, echo=True)

    class Table(Base):
        __tablename__ = 'BDIDXINDEXES'
        # 定义各字段
        FIDXID = sa.Column(sa.String(200), primary_key=True)
        FCRAWLID = sa.Column(sa.String(200))
        FAREANM = sa.Column(sa.String(200))
        FKEYWORD = sa.Column(sa.String(200))
        FIDXDTKEY = sa.Column(sa.String(200))
        FIDXVAL = sa.Column(sa.Numeric(16,4))
        FIDXDT = sa.Column(sa.Date)
        FCREATEDT = sa.Column(sa.Date)
        FLASTUPDDT = sa.Column(sa.Date)

    Base.metadata.create_all(engine)


if __name__ == "__main__":
    create_table()
    logger = MyLoger(log_conf, __name__)
    run_date_list = check_run_date()
    bdis = BaiduIndexSpider(run_date_list=run_date_list, **conf)
    bdis.start_cral()
