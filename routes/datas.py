import json
import requests
import time

from flask import Blueprint, abort, render_template, request
from models.Data import Gateway, Sensor, Datas, LeweiUsers

from config import lewei_url
from universal_func import login_required


main = Blueprint('datas', __name__)


@main.route("/update-datas/<int:user_id>", methods=["GET"])
def update_datas(user_id):
    if not user_id:
        return abort(404)
    lw_usr = LeweiUsers.query.filter_by(id=user_id).one()
    user_key = lw_usr.user_key
    sensors = Sensor.query.all()
    for sensor in sensors:
        if sensor.latest_time:
            begin_time = time.localtime(sensor.latest_time)
        else:
            # start time: 1519833600 2018-03-01
            # time gap: 1522512000 2018-04-01
            begin_time = time.localtime(1519833600)
        save_data(begin_time, sensor, user_key)
    return "OK"


@main.route("/update-equip/<int:user_id>", methods=["GET"])
def update_equip(user_id):
    if not user_id:
        return abort(404)
    lw_usr = LeweiUsers.query.filter_by(id=user_id).one()
    url = lewei_url["all_equip"]
    headers = {"userkey": lw_usr.user_key}
    gateway_list = json.loads(requests.get(url, headers=headers).content.decode("utf-8"))
    for form in gateway_list:
        gw = Gateway(form)
        if not Gateway.query.filter_by(gateway_id=gw.gateway_id).all():
            gw.lewei_user = lw_usr
            gw.save()
        else:
            gw = Gateway.query.filter_by(gateway_id=gw.gateway_id).one()

        for sensor in form["sensors"]:
            ss = Sensor(sensor)
            if not Sensor.query.filter_by(sensor_id=ss.sensor_id).all():
                ss.gateway = gw
                ss.save()
    return "OK"


@main.route("/index", methods=["GET", "POST"])
@login_required
def datas():
    if request.method.upper() == "GET":
        today = time.strftime("%Y-%m-%d", time.localtime())
        str_time = time.strptime(today, "%Y-%m-%d")
        start_time = time.mktime(str_time)
        end_time = time.time()
        sensors = Sensor.query.all()
        data_list = Datas.query.filter(Datas.time > start_time, Datas.time < end_time,
                                       Datas.sensor_id == sensors[0].id).all()
        date_times = []
        datas = []
        for data in data_list:
            date_times.append(data.print_time)
            datas.append(data.value)
        return render_template("/datas/datas.html", x_datas=json.dumps(date_times), y_datas=json.dumps(datas),
            sensors=sensors)

    else:
        start_time = request.form.get("start_time", "")
        end_time = request.form.get("end_time", "")
        sensor_id = int(request.form.get("sensor_id", ""))

        sensor = Sensor.query.filter_by(id=sensor_id).one()

        start_time = time.mktime(time.strptime(start_time, "%Y-%m-%d %H:%M:%S"))
        end_time = time.mktime(time.strptime(end_time, "%Y-%m-%d %H:%M:%S"))
        data_list = Datas.query.filter(Datas.time > start_time, Datas.time < end_time,
                                       Datas.sensor_id == sensor_id).all()
        date_times = []
        datas = []
        for data in data_list:
            date_times.append(data.print_time)
            datas.append(data.value)
        d = {}
        d["date_times"] = date_times
        d["datas"] = datas
        d["sensor_name"] = sensor.name
    return json.dumps(d)


@main.route("/test", methods=["GET"])
def teest():
    pass


def save_data(begin_time, sensor, user_key):
    headers = {"userkey": user_key}
    now = time.time()
    end_time = time.mktime(begin_time)
    while end_time < now:
        middle_time = time.localtime(end_time)
        end_time += 1522512000 - 1519833600
        if end_time > now:
            end_time = now
        e_time = time.localtime(end_time)
        mt = middle_time
        et = e_time
        url = lewei_url["get_data"].format(sensor_id=sensor.sensor_id, s_year=mt.tm_year, s_month=mt.tm_mon,
            s_day=mt.tm_mday, s_hour=mt.tm_hour, s_min=mt.tm_min, s_sec=mt.tm_sec, e_year=et.tm_year,
            e_month=et.tm_mon, e_day=et.tm_mday, e_hour=et.tm_hour, e_min=et.tm_min, e_sec=et.tm_sec)
        content = requests.get(url, headers=headers).content.decode("utf-8")
        data_list = json.loads(content)["Data"]
        if data_list:
            for form in data_list:
                data = Datas(form)
                data.sensor = sensor
                data.save()
            sensor.latest_time = end_time
            sensor.save()
