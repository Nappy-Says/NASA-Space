from models.models import Satellite
from flask import Blueprint, request, jsonify


bp = Blueprint(
    name = 'satellite',
    import_name = 'satellite',
    url_prefix = '/v1/'
)


# print(24 / orb.tle.mean_motion)


@bp.route('/satellite/get')
def get_list_of_satellites():
    _page = request.args.get('page', -1)

    if _page == -1:
        return jsonify({'message': 'Missing parametrs'}), 400
    

    last_count_data = (int(_page)-1) * 20
    next_satellites_data = last_count_data + 20

    satellites_in_count_page = Satellite.select().where(
        Satellite.id.between(last_count_data, next_satellites_data))

    data = []
    for i in satellites_in_count_page:
        data.append({
            'id': i.id,
            'name': i.name
        })

    return jsonify(data), 200


@bp.route('/sputniks/status/', methods=['PATCH'])
def patch_sputnik_show_status():
    _status = request.args.get('status', -1)

    if _status == -1:
        return jsonify({'message': 'Missing parametrs'}), 400

    # BLOCK IN SOCKETS
