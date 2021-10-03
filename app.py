from flask import Flask
from flask_cors import CORS
from configparser import ConfigParser
from utils import register_blueprints


config = ConfigParser()
config.sections()
config.read('config.ini')


app = Flask(__name__)
app.config['SECRET_KEY'] = config['keys']['secret_app']
register_blueprints(app)
CORS(app)


if __name__ == '__main__':
    app.run(
        debug=True,
        host=config['network']['host'],
        port=config['network']['port']
    )
