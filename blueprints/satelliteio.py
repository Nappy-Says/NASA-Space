
from models.models import *
from datetime import datetime
from time import mktime, sleep
from utils import get_more_data
from pyorbital.orbital import Orbital
from flask import Blueprint, request, jsonify


# Temp active objects
orbit = []

bp = Blueprint(
    name = 'satelliteio',
    import_name='satelliteio',
    url_prefix = '/v1/'
)


@bp.route('/add', methods=['POST'])
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


@bp.route('/remove', methods=['DELETE'])
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


@bp.route('/settime', methods=['POST'])
def set_time():
    """
    Setting a specific time and day (teleportation in time)
    """
    _seconds = request.args.get('seconds', -1)
    
    if _seconds == -1:
        return jsonify({'message': 'Missing parametrs'}), 400


    get_detail_data_about_object(_seconds)


@bp.route('/get')
def get_detail_data_about_object(timeseconds=0):
    """
    Sending detailed information about each satellite (or another object)

    * Mode:
        - reverse
        - stream real-time
        - forward
    """
    
    now = int(mktime(datetime.now().timetuple()))
    allseconds = now+timeseconds
    datestamp = datetime.fromtimestamp(allseconds)

    day = datestamp.day
    hour = datestamp.hour
    year = datestamp.year
    month = datestamp.month
    minute = datestamp.minute
    second = datestamp.second

    sleep(1)

    dtobj = datetime(year, month, day, hour, minute, second)
    dataa = get_more_data(dtobj)

    return jsonify(dataa), 200
