from time import sleep
import requests
import configparser

config = configparser.ConfigParser()
config.sections()
config.read('config.ini')

while True:
    r = requests.get('https://127.0.0.1:5000/satelliteio/get')
    print(r.content)


    # sleep(1)
