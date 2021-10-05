import socket
import socketio
from json import dumps
from models.models import *
from flask_cors import CORS
from datetime import datetime
from time import mktime, sleep
from flask_socketio import SocketIO
from pyorbital.orbital import Orbital
from configparser import ConfigParser
from flask import Flask, request, jsonify
from utils import register_blueprints, identification_of_type_of_object

config = ConfigParser()
config.sections()
config.read('config.ini')

app = Flask(__name__)
socket = SocketIO(app, cors_allowed_origins="*")
# socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


# app.wsgi_app = socketio.WSGIApp(socket, app.wsgi_app)
app.secret_key = config['keys']['secret_app']
register_blueprints(app)
CORS(app)

# Temp active objects
orbit = []
temp_time_data = {
    'teleport': 0,
    'status': 'stream',
    'saved_time': int(mktime(datetime.now().timetuple())),
    'speed': 1
}

save_time = int(mktime(datetime.now().timetuple()))
now_time = int(mktime(datetime.now().timetuple()))


def object_filter(dtobj, type):
    global orbit

    data = {
        "date": str(dtobj).split()[0],
        "time": str(dtobj).split()[1],
        "data": []
    }

    # datastr3 =
    # datastr += f"'date':{str(dtobj).split()[0]},'time':{str(dtobj).split()[1]},'data':["
    # datastr2 = f'{str(dtobj).split()[0]}&{str(dtobj).split()[1]}'

    for i in orbit:
        try:
            typee = identification_of_type_of_object(list(i.keys())[0])

            if typee == type or type == 'all':
                val = list(i.values())[0].get_lonlatalt(dtobj)
                # datastr += f"'id':{list(i.keys())[0]},'type':{typee},'x':{str(val[0])[:str(val[0]).find('.')+5]},'y':{str(val[1])[:str(val[1]).find('.')+5]},'z':{str(val[2])[:str(val[2]).find('.')+5]}"

                # ss = {
                #     'id': list(i.keys())[0],
                #     'type': typee,
                #     'x': str(val[0])[:str(val[0]).find('.')+5],
                #     'y': str(val[1])[:str(val[1]).find('.')+5],
                #     'z': str(val[2])[:str(val[2]).find('.')+5]
                # }
                # datastr3.append(str(ss))

                data["data"].append({
                    "id": list(i.keys())[0],
                    "type": typee,
                    "x": str(val[0])[:str(val[0]).find('.')+5],
                    "y": str(val[1])[:str(val[1]).find('.')+5],
                    "z": str(val[2])[:str(val[2]).find('.')+5]
                })

                # datastr2 += f"&{list(i.keys())[0]}&{typee}&{str(val[0])[:str(val[0]).find('.')+5]}&{str(val[1])[:str(val[1]).find('.')+5]}&{str(val[2])[:str(val[2]).find('.')+5]}"

        except Exception as err:
            print(err, 'object_filte()')
            pass

    data = str(data).replace("'", '"')

    return data


@app.route('/v1/satelliteio/add', methods=['POST'])
def add_object():
    """
    Adding a new active satellite (or another object) to the general temporary list
    """

    _id = request.args.get('id', -1)
    if _id == -1:
        return jsonify({'message': 'Missing parametrs'}), 400

    satellite = Satellite.get_or_none(Satellite.id == _id)
    if not satellite:
        return jsonify({'message': 'TLE not fond'}), 404

    lines = Lines.select().where(Lines.satellite == satellite.id)

    try:
        _orbit = Orbital(satellite=satellite.name,
                         line1=lines[0].line, line2=lines[1].line)
    except Exception as err:
        print(err, _id)
        return jsonify({'message': f'{err} {_id}'}), 500

    global orbit
    for i in orbit:
        if _id in list(i.keys()):
            return jsonify({'message': 'Such a satellite is already on the map'}), 409

    try:
        _orbit.get_lonlatalt(datetime.now())
    except Exception as err:
        print(err)
        return jsonify({'message': f'{err}, {_id}'}), 500

    orbit.append({_id: _orbit})

    return jsonify({'message': str(orbit)}), 200


@app.route('/v1/satelliteio/remove', methods=['DELETE'])
def remove_object():
    """
    Remove satellite (or another object) information from the active list
    """
    _id = request.args.get('id', -1)
    if _id == -1:
        return jsonify({'message': 'Missing paramerts'}), 400

    for i in range(len(orbit)):
        if _id in list(orbit[i].keys())[0]:
            orbit.pop(i)
            return jsonify({'message': 'OK'}), 200

    return jsonify({'message': 'Satellite not found'}), 404


def fnc(status='0'):
    global temp_time_data
    global now_time
    global save_time

    lst = save_time
    speed = temp_time_data['speed']
    status = temp_time_data['status']

    if status == 'pause':
        now_time += 1
        return datetime.fromtimestamp(lst)

    if status == 'backward':
        now = int(mktime(datetime.now().timetuple()))
        return datetime.fromtimestamp(lst - (now - now_time) * speed)

    if status == 'forward':
        now = int(mktime(datetime.now().timetuple()))
        return datetime.fromtimestamp(lst + (now - now_time) * speed)

    return datetime.fromtimestamp(int(mktime(datetime.now().timetuple())))


@socket.on('connect')
def connect():
    print('connected')


@socket.event
def get_detail_data_about_object(setArg):
    """
    Sending detailed information about each satellite (or another object)

    * Mode:
        - reverse
        - stream real-time
        - forward
    """
    print(dumps(setArg), 'asdasdasd')
    global orbit, temp_time_data, temp_time_data, save_time, now_time

    _status = setArg.get('status', 'all')
    _time = setArg.get('seconds', 0)
    _speed = setArg.get('speed', 0)

    if _speed != 0:
        temp_time_data['speed'] = _speed

    if _status == 'stream' or _status == 'reset':
        temp_time_data['status'] = _status
        save_time = int(mktime(datetime.now().timetuple()))

    if _time >= 0:
        save_time = _time
        now_time = _time
    else:
        save_time = int(mktime(fnc().timetuple()))
        now_time = int(mktime(datetime.now().timetuple()))

    temp_time_data['status'] = _status

    while True:
        datetimetamp = fnc()

        day = datetimetamp.day
        hour = datetimetamp.hour
        year = datetimetamp.year
        month = datetimetamp.month
        minute = datetimetamp.minute
        second = datetimetamp.second

        sleep(1)

        dtobj = datetime(year, month, day, hour, minute, second)
        dataa = object_filter(dtobj, 'all')

        socket.emit('location', dataa)


@app.route('/v1/satelliteio/get')
def get_detail_data_about_object():
    """
    Sending detailed information about each satellite (or another object)

    * Mode:
        - reverse
        - stream real-time
        - forward
    """
    # datetimetamp = datetime.fromtimestamp(int(
    # mktime(datetime.now().timetuple())))
    global temp_time_data

    datetimetamp = fnc()

    print(temp_time_data)

    day = datetimetamp.day
    hour = datetimetamp.hour
    year = datetimetamp.year
    month = datetimetamp.month
    minute = datetimetamp.minute
    second = datetimetamp.second

    sleep(1)

    dtobj = datetime(year, month, day, hour, minute, second)
    dataa = object_filter(dtobj, 'all')

    return jsonify(str(dataa).replace(' ', '')), 200


if __name__ == '__main__':
    socket.run(app, host='192.168.0.119', port=8000, debug=True)
    # app.run(host='192.168.0.119', port=8000, debug=True)


# http://103.246.146.95:5000/v1/satelliteio/get
    