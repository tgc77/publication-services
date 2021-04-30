from flask import render_template, abort
from flask_socketio import emit

from . import bp, rpc, socket, client_consumer


@socket.on('request_publication')
def request_publication():
    try:
        if client_consumer.publications_count() > client_consumer.max_size:
            emit('reset_data')

        publication = client_consumer.consume_publication()
        if publication is not None:
            emit('new_publication', str(publication))
    except Exception as e:
        print('Oopss!', e)


@bp.route('/')
@bp.route('/index')
def index():
    return render_template('index.html.j2', title='BYNE Test - Client')


@bp.route('/history', methods=['GET'])
def history():
    try:
        history = rpc.service4.get_history()
        return render_template('history.html.j2',
                               title='History Result', history=history)
    except Exception as e:
        print('Ooops! ', e)
        abort(400, error=e)
