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
