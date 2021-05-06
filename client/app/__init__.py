from flask import Flask, Blueprint
from nameko.standalone.rpc import ServiceRpcProxy
from flask_socketio import SocketIO
from flask_redis import FlaskRedis

from .config import Config
from .client_consumer import ClientConsumer

bp = Blueprint('app', __name__)
socket = SocketIO()
redis_client = FlaskRedis(decode_responses=True, charset='utf-8')
client_consumer = ClientConsumer(max_size=20)


def rpc_proxy() -> ServiceRpcProxy:
    """
    Service RPC Proxy to connect to service data provider.

    Returns:
        ServiceRpcProxy: Service RPC Proxy connector.
    """
    return ServiceRpcProxy(Config.SERVICE_PROVIDER, Config.SERVICE_CONFIG)


def create_app(config_class=Config) -> Flask:
    """
    Flask factory App creation to initialize dependencies.

    Args:
        config_class (object, optional): Flask config parameters.

    Attibutes:
        bp (Blueprint): Route Factory pattern object.
        rpc (FlaskPooledClusterRpcProxy): Flask RpcProxy Nameko service connector.
        socket (SocketIO): Websocket to receive real-time data incoming from service.
        redis_client (FlaskRedis): Flask Redis connector object.
        client_consumer (ClientConsumer): Microservice client connector.
    Returns:
        [Flask]: Flask app instance
    """
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.register_blueprint(bp)
    socket.init_app(app, cors_allowed_origins="*")
    redis_client.init_app(app)
    client_consumer.init_app(redis_client)

    return app


from . import routes  # nopep8
