import sys
from io import BytesIO
import requests
from PIL import Image
from zadacha1.size import get_span

addres = " ".join(sys.argv[1:])
server = "http://geocode-maps.yandex.ru/1.x/"
req_params = {
    "apikey": "8013b162-6b42-4997-9691-77b7074026e0",
    "geocode": addres,
    "format": "json"
}
res = requests.get(server, params=req_params)
if not res:
    sys.exit(1)
data = res.json()
toponym = data["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
pos = toponym["Point"]["pos"]
cords = pos.split(" ")
span = get_span(toponym)
map_server = "https://static-maps.yandex.ru/v1"
map_params = {
    "ll": f"{cords[0]},{cords[1]}",
    "spn": span,
    "apikey": "f3a0fe3a-b07e-4840-a1da-06f18b2ddf13",
    "pt": f"{cords[0]},{cords[1]},pm2dgl"
}
map_res = requests.get(map_server, params=map_params)
pic_data = BytesIO(map_res.content)
pic = Image.open(pic_data)
pic.show()