# -*- coding: utf-8 -*-
import time

from . import ModelMixin
from . import db


class Gateway(db.Model, ModelMixin):
    __tablename__ = "gateways"
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}
    id = db.Column(db.Integer, primary_key=True)
    gateway_id = db.Column(db.Integer)
    name = db.Column(db.String(32))
    lewei_user_id = db.Column(db.Integer(), db.ForeignKey("leweiusers.id"))
    lewei_user = db.relationship("LeweiUsers", backref=db.backref('gateways'), lazy=True)

    def __init__(self, form):
        self.gateway_id = form.get("id", "")
        self.name = form.get("name", "")


class Sensor(db.Model, ModelMixin):
    __tablename__ = "sensors"
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    sensor_id = db.Column(db.Integer)
    gateway_id = db.Column(db.Integer, db.ForeignKey("gateways.id"))
    gateway = db.relationship("Gateway", backref=db.backref('sensors', lazy=True))
    latest_time = db.Column(db.Float(precision=53))

    def __init__(self, form):
        self.sensor_id = form.get("id", "")
        self.name = form.get("name", "")
        self.latest_time = None


class Datas(db.Model, ModelMixin):
    __tablename__ = "datas"
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.Float(precision=53))
    print_time = db.Column(db.String(32))
    value = db.Column(db.Float(precision=53))
    sensor_id = db.Column(db.Integer, db.ForeignKey("sensors.id"))
    sensor = db.relationship("Sensor", backref=db.backref('datas', lazy=True))

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


class LeweiUsers(db.Model, ModelMixin):
    __tablename__ = "leweiusers"
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32))
    user_key = db.Column(db.String(64))

    def __init__(self, form):
        self.username = form.get("username")
        self.user_key = form.get("user_key", "")
