from werkzeug.utils import find_modules, import_string


def register_blueprints(app):
    """
    Register satellite module
    """
    for name in find_modules('blueprints'):
        mod = import_string(name)
        if hasattr(mod, 'bp'):
            app.register_blueprint(mod.bp)


