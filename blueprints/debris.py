from flask import Blueprint, request, jsonify


bp = Blueprint(
    name = 'debris',
    import_name = 'debris',
    url_prefix = '/v1/'
)


@bp.route('/debris/status/', methods=['PATCH'])
def patch_debris_show_status():
    _status = request.args.get('status', -1)

    if _status == -1:
        return jsonify({'message': 'Missing parametrs'}), 400

    # BLOCK IN SOCKETS
