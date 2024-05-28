import contextlib
import datetime

from sqlalchemy import Column, DateTime, Float, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from nt_house_info_spider.static import constant

engine = create_engine(
    constant.SQLALCHEMY_DATABASE_URI,  # SQLAlchemy 数据库连接串
    echo=bool(constant.SQLALCHEMY_ECHO),  # 是否要把所执行的SQL打印出来，一般用于调试
    pool_size=int(constant.SQLALCHEMY_POOL_SIZE),  # 连接池大小
    max_overflow=int(constant.SQLALCHEMY_POOL_MAX_SIZE),  # 连接池最大的大小
    pool_recycle=int(constant.SQLALCHEMY_POOL_RECYCLE),  # 多久时间主动回收连接
)
Session = sessionmaker(bind=engine)
Base = declarative_base()


class BaseMixin(object):
    """model的基类,所有model都必须继承"""

    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime, nullable=False, default=datetime.datetime.now)
    updated_at = Column(
        DateTime,
        nullable=False,
        default=datetime.datetime.now,
        onupdate=datetime.datetime.now,
        index=True,
    )
    deleted_at = Column(DateTime)  # 可以为空, 如果非空, 则为软删


class HouseInfo(Base, BaseMixin):  # type: ignore [valid-type, misc]
    __tablename__ = "house_info"

    pk = Column(Integer, unique=True)
    name = Column(String(50), nullable=False)
    location = Column(String(30), nullable=False)
    floor = Column(String(3), nullable=False)
    total_floor = Column(Integer, nullable=False)
    house_layout = Column(String(10), nullable=False)
    house_area = Column(Float, nullable=False)
    house_dir = Column(String(3), nullable=False)
    total_price = Column(Float, nullable=False)
    unit_price = Column(Integer, nullable=False)
    follower_num = Column(Integer, nullable=False)
    upload_time = Column(String(10), nullable=False)


Base.metadata.create_all(engine)


@contextlib.contextmanager
def get_session():
    """
    获取一个数据库会话对象，并在会话结束时自动提交或回滚事务。

    Args:
        无

    Returns:
        Session: 数据库会话对象。

    Raises:
        Exception: 如果在数据库操作中发生异常，则抛出异常。

    """

    s = Session()
    try:
        yield s
        s.commit()
    except Exception as e:
        s.rollback()
        raise e
    finally:
        s.close()
