from datetime import date, datetime
import requests

p = 0
pp = 0

d = datetime.now()
for i in range(1000000000000000):
    r = requests.post(f'http://192.168.0.119:8000/v1/satelliteio/add?id={i+1}')

    if r.status_code == 200:
        p += 1
    elif r.status_code == 404:
        break
    else:
        pp += 1
    print(r, p, pp)
print(r, p, pp, d, datetime.now())
