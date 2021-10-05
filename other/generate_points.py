import requests

p = 0
pp = 0

for i in range(1000000000000000):
  r = requests.post(f'http://127.0.0.1:5000/v1/satelliteio/add?id={i}')

  if r.status_code == 200:
    p+=1
  else:
    pp+=1
  print(r, p, pp)
