import time

from contextlib import closing

from sqlalchemy import Column, String, create_engine, Integer, ForeignKey, Float
from sqlalchemy.orm import sessionmaker, relationship, backref
from sqlalchemy.ext.declarative import declarative_base

from config import db_uri
from models import ModelMixin

# 创建对象的基类:
db = declarative_base()


class Gateway(db, ModelMixin):
    __tablename__ = "gateways"
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}
    id = Column(Integer, primary_key=True)
    gateway_id = Column(Integer)
    name = Column(String(32))
    username = Column(String(32))

    def __init__(self, form):
        self.gateway_id = form.get("id", "")
        self.name = form.get("name", "")
        self.username = None


class Sensor(db, ModelMixin):
    __tablename__ = "sensors"
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}
    id = Column(Integer, primary_key=True)
    name = Column(String(32))
    sensor_id = Column(Integer)
    gateway_id = Column(Integer, ForeignKey("gateways.id"))
    gateway = relationship("Gateway", backref=backref('sensors', lazy=True))

    def __init__(self, form):
        self.sensor_id = form.get("id", "")
        self.name = form.get("name", "")


class Datas(db, ModelMixin):
    __tablename__ = "datas"
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}
    id = Column(Integer, primary_key=True)
    time = Column(Float(precision=53))
    print_time = Column(String(32))
    value = Column(Float(precision=53))
    sensor_id = Column(Integer, ForeignKey("sensors.id"))
    sensor = relationship("Sensor", backref=backref('datas', lazy=True))

    def __init__(self, form):
        self.print_time = form.get("updateTime", None)
        self.time = self.get_time()
        self.value = form.get("value", )

    def get_time(self):
        if self.print_time:
            strptime = time.strptime(self.print_time, "%Y/%m/%d %H:%M:%S")
            time_stamp = time.mktime(strptime)
            return float(time_stamp)
        else:
            pass

# 初始化数据库连接:
engine = create_engine(db_uri)
# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)

with closing(DBSession()) as session:
    a = session.query(Gateway).filter(Gateway.id == 3).first()
    print(a.sensors)
    # d = {
    #     ""
    # }
