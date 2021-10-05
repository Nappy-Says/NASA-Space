import socketio
import configparser
from datetime import datetime

config = configparser.ConfigParser()
config.sections()
config.read('config.ini')

socket_io = socketio.Client()
# socket_io.connect(config['conf']['ip_address'])
socket_io.connect('http://0.0.0.0:8000/')
second = 57600


@socket_io.event
def connect():
    print('connect')

    global second
    second += 1

    socket_io.emit(
        'get_detail_data_about_object', {'status': 'stream'})


@socket_io.event
def disconnect():
    print('disconnected')


@socket_io.on('location')
def get_location_handler(arg1):
    print('Data: ', arg1)
