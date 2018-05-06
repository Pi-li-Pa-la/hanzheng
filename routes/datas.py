import json
import requests

from flask import Blueprint, request
from models.Data import Gateway, Sensor, Datas


main = Blueprint('datas', __name__)
headers = {
    "userkey": "6204472cfcc94a81b90e8d22773ca99e",
}


@main.route("/update-datas/<string:sensor_id>", methods=["POST"])
def update_datas(sensor_id):
    data_list = json.loads(request.get_json())["Data"]
    sensor = Sensor.query.filter_by(sensor_id=sensor_id).first()
    for data_dict in data_list:
        new_data = Datas(data_dict)
        # all = sensor.datas
        # print(all)
        new_data.sensor = sensor
        new_data.save()
    return "OK"

@main.route("/update-equip/<string:username>", methods=["POST"])
def update_equip(username):
    equip_list = json.loads(request.get_json())
    for gateway in equip_list:
        gw = Gateway(gateway)
        gw.save()
        for sensor in gateway["sensors"]:
            ss = Sensor(sensor)
            ss.gateway = gw
            ss.save()
    return "OK"


@main.route("/get-all-update", methods=["GET"])
def get_all_update():

    json_str = get_all_gateway_json(headers)
    gateway_list = json.loads(json_str)
    for gateway in gateway_list:

        # update equips
        gw = Gateway(gateway)
        gw.save()
        for sensor in gateway["sensors"]:
            ss = Sensor(sensor)
            ss.gateway = gw
            # ss.save()

        # update datas
        for sensor in gateway["sensors"]:
            sensor_id = sensor["id"]
            url = "http://www.lewei50.com/api/v1/sensor/gethistorydata/{}".format(sensor_id)
            r = requests.get(url, headers=headers)
            data_list = json.loads(r.content)["Data"]
            sensor = Sensor.query.filter_by(sensor_id=sensor_id).first()
            for data_dict in data_list:
                new_data = Datas(data_dict)
                new_data.sensor = sensor
                # new_data.save()
            return "OK"


def get_all_gateway_json(headers):
    url = "http://www.lewei50.com/api/v1/user/getsensorswithgateway"
    r = requests.get(url, headers=headers)
    json_str = r.content.decode("utf-8")
    return json_str



