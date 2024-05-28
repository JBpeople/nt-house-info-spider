# 数据库配置
SQLALCHEMY_DATABASE_URI = "sqlite:///nt_house_info_spider/db/data.db"
SQLALCHEMY_ECHO = False
SQLALCHEMY_POOL_SIZE = 50
SQLALCHEMY_POOL_MAX_SIZE = 100
SQLALCHEMY_POOL_RECYCLE = 3600

# 爬虫配置
URL = "https://nt.ke.com/ershoufang/y1/"
