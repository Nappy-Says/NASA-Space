import socketio
import configparser
from datetime import datetime

config = configparser.ConfigParser()
config.sections()
config.read('config.ini')

socket_io = socketio.Client()
socket_io.connect(config['conf']['ip_address'])
second = 57600




@socket_io.event
def connect():
    print('time acceleration')

    global second
    second+=1

    socket_io.emit(
        'location_handler_time_multiply_acceleration', second)



@socket_io.event
def disconnect():
    print('disconnected')



@socket_io.on('location')
def get_location_handler(arg1):
    print('Data: ', arg1)
