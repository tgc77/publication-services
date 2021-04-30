from flask import Flask, Blueprint
from flask_nameko import FlaskPooledClusterRpcProxy
from flasgger import Swagger, swag_from
from flask_socketio import SocketIO
from flask_redis import FlaskRedis

from .config import Config
from .client_consumer import ClientConsumer

bp = Blueprint('app', __name__)
rpc = FlaskPooledClusterRpcProxy()
socket = SocketIO()
redis_client = FlaskRedis(decode_responses=True, charset='utf-8')
client_consumer = ClientConsumer(max_size=20)


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.register_blueprint(bp)
    Swagger(app)
    try:
        rpc.init_app(app)
        socket.init_app(app, cors_allowed_origins="*")
        redis_client.init_app(app)
    except Exception as e:
        print('Poouts!', e)

    return app


from . import routes, errors  # nopep8
