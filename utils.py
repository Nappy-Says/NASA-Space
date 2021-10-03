from models.models import Satellite
from werkzeug.utils import find_modules, import_string


def register_blueprints(app):
    """
    Register satellite module
    """
    for name in find_modules('blueprints'):
        mod = import_string(name)
        if hasattr(mod, 'bp'):
            app.register_blueprint(mod.bp)


def identification_of_type_of_object(objID):
    obj = Satellite.get(Satellite.id == objID).name

    if obj.find('DEB') > 0:
        return 'debris'
    if obj.find('R/B') > 0:
        return 'rocket body'
    if obj.find('TBA') > 0:
        return 'other'
    
    return 'satellite'


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
