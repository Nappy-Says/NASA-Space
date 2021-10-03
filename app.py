import time

import socketio
from utils import *
from models.models import *
from flask_cors import CORS
from datetime import datetime
from flask_socketio import SocketIO
from configparser import ConfigParser
from pyorbital.orbital import Orbital
from pyorbital.orbital import OrbitalError
from flask import Flask, request, jsonify


app = Flask(__name__)
app.config['SECRET_KEY'] = 'SZWAQ@AWSErfr6GYuijmo(I*UYTDRXCTVB{+_{":?><MN'
register_blueprints(app)
CORS(app)

socket = SocketIO(app, cors_allowed_origins="*")
# socket = socketio.Server(cors_allowed_origins='*')
# app.wsgi_app = socketio.WSGIApp(socket, app.wsgi_app)

config = ConfigParser()
config.sections()
config.read('config.ini')

orbit = []


def get_more_data(dtobj):
    global orbit

    data = []
    for i in orbit:

        val = list(i.values())[0].get_lonlatalt(dtobj)

        print(orbit, 'asdawdwoedsv')
        print(list(i.values())[0], 'asdawdwoedsv')

        data.append({
            'id': list(i.keys())[0],
            'date': str(dtobj).split()[0],

            'time': str(dtobj).split()[1],
            'type': '',

            'x': val[0],
            'y': val[1],
            'z': val[2]
        })

    return data


@app.route('/v1/satelliteio/add', methods=['POST'])
def add():
    _id = request.args.get('id', -1)
    if _id == -1:
        return jsonify({'message': 'Missing parametrs'}), 400

    satellite = Satellite.get_or_none(Satellite.id == _id)
    if not satellite:
        return jsonify({'message': 'TLE not fond'}), 404

    global orbit
    lines = Lines.select().where(Lines.satellite == satellite.id)

    print(_id, satellite.id, satellite.name, lines)

    _orbit = Orbital(satellite=satellite.name,
                     line1=lines[0].line, line2=lines[1].line)

    for i in orbit:
        if _id in list(i.keys()):
            return jsonify({'message': 'Such a satellite is already on the map'}), 409

    orbit.append({_id: _orbit})

    return jsonify({'message': str(orbit)}), 200


@app.route('/v1/satelliteio/remove', methods=['DELETE'])
def remove_object():
    _id = request.args.get('id', -1)
    if _id == -1:
        return jsonify({'message': 'Missing paramerts'}), 400

    for i in range(len(orbit)):
        if _id in list(orbit[i].keys())[0]:
            orbit.pop(i)
            return jsonify({'message': 'OK'}), 200

    return jsonify({'message': 'Satellite not found'}), 404


@app.route('/v1/satelliteio/settime', methods=['POST'])
def set_time():
    _seconds = request.args.get('seconds')
    get(int(_seconds))


# @socket.event
# def connect():
#     print('CLIENT IS CONNECTED')


# @socket.on('location_handler_time_multiply_acceleration')
# def get(timeseconds):
#     print('Received data: ', timeseconds)

#     while True:
#         now = int(time.mktime(datetime.now().timetuple()))
#         allseconds = now+timeseconds
#         datestamp = datetime.fromtimestamp(allseconds)

#         day = datestamp.day
#         hour = datestamp.hour
#         year = datestamp.year
#         month = datestamp.month
#         minute = datestamp.minute
#         second = datestamp.second

#         socket.sleep(1)

#         dtobj = datetime(year, month, day, hour, minute, second)
#         dtobj2 = datetime(year, month, day, hour+5, minute, second)
#         dataa = get_more_data(dtobj)

#         print(get_more_data(dtobj2))

#         socket.emit('location', 'list(dataa)')


# @socket.on('location')
# def ll(s):
#     print(s)


@app.route('/v1/satelliteio/get')
def route(timeseconds=0):
    now = int(time.mktime(datetime.now().timetuple()))
    allseconds = now+timeseconds
    datestamp = datetime.fromtimestamp(allseconds)

    day = datestamp.day
    hour = datestamp.hour
    year = datestamp.year
    month = datestamp.month
    minute = datestamp.minute
    second = datestamp.second

    socket.sleep(1)

    dtobj = datetime(year, month, day, hour, minute, second)
    dataa = get_more_data(dtobj)

    return jsonify(dataa), 200


if __name__ == '__main__':
    app.run(
        debug=True,
        host=config['conf']['host'],
        port=5000
    )
