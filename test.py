import requests
import json

headers = {
    "userkey": "6204472cfcc94a81b90e8d22773ca99e",
}

# 34787, 34796, 35048
url = "http://www.lewei50.com/api/v1/sensor/gethistorydata/63561"
# url = "http://www.lewei50.com/api/v1/user/getsensorswithgateway"

r = requests.get(url, headers=headers)
response = json.loads(r.content.decode("utf-8"))
print(response)
# for data in response:
    # print(data)
    # for k, v in data.items():
    #     print(k, ": ", v)
    # print("\n\n")
# print(r.content)
