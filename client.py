import requests
import json

headers = {
    "userkey": "6204472cfcc94a81b90e8d22773ca99e",
}


def get_all_gateway_json(headers):
    url = "http://www.lewei50.com/api/v1/user/getsensorswithgateway"
    r = requests.get(url, headers=headers)
    json_str = r.content.decode("utf-8")
    return json_str


def update_gateway():
    json_str = get_all_gateway_json(headers)
    rsp = requests.post("http://www.iotxy.top/datas/update-equip/{}".format("poisonhz"), json=json_str)
    print(rsp)


def update_datas():
    json_str = get_all_gateway_json(headers)
    gateway_list = json.loads(json_str)
    for gateway in gateway_list:
        for sensor in gateway["sensors"]:
            sensor_id = sensor["id"]
            url = "http://www.lewei50.com/api/v1/sensor/gethistorydata/{}".format(sensor_id)
            r = requests.get(url, headers=headers)
            json_str = r.content.decode("utf-8")
            rsp = requests.post("http://www.iotxy.top/datas/update-datas/{}".format(sensor_id), json=json_str)
            print(rsp)


if __name__ == "__main__":
    update_gateway()
    update_datas()
    # url = "http://www.lewei50.com/api/v1/sensor/gethistorydata/{}".format(63574)
    # r = requests.get(url, headers=headers)
    # json_str = r.content.decode("utf-8")
    # data_list = json.loads(json_str)["Data"]
    # rsp = requests.post("http://0.0.0.0:3000/datas/update-datas/{}".format("63574"), json=json_str)
