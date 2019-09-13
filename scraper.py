import requests
import ujson
import settings


data = requests.get(settings.ONLINER_URL)
apartments = data.json()["apartments"]

last_id = 0
with open("last_id", "r") as f:
    last_id = int(f.read())

new_last_id = apartments[0]["id"]
with open("last_id", "w") as f:
    f.write(str(new_last_id))

with open("need_broadcast", "w") as f:
    need_broadcast_apartments = filter(lambda apartment: apartment["id"] > last_id, apartments)
    for apartment in need_broadcast_apartments:
        f.write(f"{ujson.dumps(apartment)}\n")
