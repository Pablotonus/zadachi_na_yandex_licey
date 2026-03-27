import sys
import math
from io import BytesIO
import requests
from PIL import Image

def get_d(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    rad = math.radians((y1 + y2) / 2.0)
    dx = math.cos(rad) * (x1 - x2) * 111000
    dy = (y1 - y2) * 111000
    return math.sqrt(dx**2 + dy**2)

addr = " ".join(sys.argv[1:])
api1 = "http://geocode-maps.yandex.ru/1.x/"
par1 = {
    "apikey": "8013b162-6b42-4997-9691-77b7074026e0",
    "geocode": addr,
    "format": "json"
}
res1 = requests.get(api1, params=par1)
if not res1:
    sys.exit(1)

data1 = res1.json()
obj = data1["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
pos = obj["Point"]["pos"].split()
x1 = float(pos[0])
y1 = float(pos[1])
api2 = "https://search-maps.yandex.ru/v1/"
par2 = {
    "apikey": "dda3ddba-c9ea-4ead-9010-f43fbc15c6e3",
    "text": "аптека",
    "lang": "ru_RU",
    "ll": f"{x1},{y1}",
    "type": "biz"
}

res2 = requests.get(api2, params=par2)
if not res2:
    sys.exit(1)
data2 = res2.json()
org = data2["features"][0]
name = org["properties"]["CompanyMetaData"]["name"]
org_addr = org["properties"]["CompanyMetaData"]["address"]
time = "Нет данных"
if "Hours" in org["properties"]["CompanyMetaData"]:
    time = org["properties"]["CompanyMetaData"]["Hours"]["text"]

org_pos = org["geometry"]["coordinates"]
x2 = float(org_pos[0])
y2 = float(org_pos[1])
d = get_d((x1, y1), (x2, y2))

print(org_addr)
print(name)
print(time)
print(round(d))

api3 = "https://static-maps.yandex.ru/v1"
par3 = {
    "apikey": "f3a0fe3a-b07e-4840-a1da-06f18b2ddf13",
    "pt": f"{x1},{y1},pm2rdm~{x2},{y2},pm2gnm"
}
res3 = requests.get(api3, params=par3)
img = BytesIO(res3.content)
pic = Image.open(img)
pic.show()