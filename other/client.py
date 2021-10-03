from time import sleep
import requests
import configparser

config = configparser.ConfigParser()
config.sections()
config.read('config.ini')

while True:
    r = requests.get(config['conf']['ip_address']+'/satelliteio/get')

    print(r.content.decode())

    sleep(1)
