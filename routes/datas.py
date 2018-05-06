import json

from flask import Blueprint, request
from models.Data import Gateway, Sensor, Datas


main = Blueprint('datas', __name__)


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