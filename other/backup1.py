from models.models import *
from datetime import datetime
from time import mktime, sleep
from pyorbital.orbital import Orbital
from flask import Blueprint, request, jsonify
from utils import identification_of_type_of_object

# Temp active objects
orbit = []
temp_time_data = {
    'teleport': 0,
    'status': 'stream',
    'saved_time': int(mktime(datetime.now().timetuple()))
}

i = 0

bp = Blueprint(
    name='satelliteio',
    import_name='satelliteio',
    url_prefix='/v1/'
)


def get_more_data(dtobj):
    global orbit

    data = {
        'date': str(dtobj).split()[0],
        'time': str(dtobj).split()[1],
        'data': []
    }

    for i in orbit:
        val = list(i.values())[0].get_lonlatalt(dtobj)
        data['data'].append({
            'id': list(i.keys())[0],

            'type': identification_of_type_of_object(list(i.keys())[0]),

            'x': val[0],
            'y': val[1],
            'z': val[2]
        })

    return data


@bp.route('/satelliteio/add', methods=['POST'])
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

    global orbit
    _orbit = Orbital(satellite=satellite.name,
                     line1=lines[0].line, line2=lines[1].line)

    for i in orbit:
        if _id in list(i.keys()):
            return jsonify({'message': 'Such a satellite is already on the map'}), 409

    orbit.append({_id: _orbit})

    return jsonify({'message': str(orbit)}), 200


@bp.route('/satelliteio/remove', methods=['DELETE'])
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


@bp.route('/satelliteio/set', methods=['POST'])
def set_status_time():
    global temp_time_data
    global i
    _status = request.args.get('status', -1)

    if _status == 'stream' or _status == -1:
        temp_time_data['status'] = _status
        temp_time_data['saved_time'] = int(mktime(datetime.now().timetuple()))
        return _status

    if _status == 'backward':
        temp_time_data['status'] = _status
        temp_time_data['teleport'] = int(mktime(datetime.now().timetuple()))
        temp_time_data['saved_time'] = int(mktime(datetime.now().timetuple()))
        print(temp_time_data)
        return _status

    if _status == 'forward':
        temp_time_data['status'] = _status
        temp_time_data['saved_time'] = temp_time_data['saved_time'] - \
            (int(mktime(datetime.now().timetuple())) -
             temp_time_data['saved_time'])
        temp_time_data['teleport'] = int(mktime(datetime.now().timetuple()))
    return _status


# now = int(mktime(datetime.now().timetuple()))
# return datetime.fromtimestamp((now+tp-lst)*-1+lst)
# i - (int(mktime(datetime.now().timetuple())) - i)

def fnc(status='0'):
    global temp_time_data
    global i
    status = temp_time_data['status']
    tp = temp_time_data['teleport']
    lst = temp_time_data['saved_time']

    print(datetime.fromtimestamp(int(mktime(datetime.now().timetuple()))))
    print(datetime.fromtimestamp(lst))

    if status == 'backward':
        now = lst
        now = int(mktime(datetime.now().timetuple()))
        return datetime.fromtimestamp(lst - (now - tp))

    if status == 'forward':
        now = int(mktime(datetime.now().timetuple()))
        return datetime.fromtimestamp(lst + (now - tp))

    return datetime.fromtimestamp(int(mktime(datetime.now().timetuple())))


@bp.route('/satelliteio/get')
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
    dataa = get_more_data(dtobj)

    return jsonify(dataa), 200
