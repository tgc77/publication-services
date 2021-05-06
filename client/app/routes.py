from flask import render_template, flash
from flask_socketio import emit

from . import (
    bp, socket, client_consumer, rpc_proxy
)


@socket.on('request_publication')
def request_publication():
    """
    Socketio event call to consume new publications incoming sending to
    front end client by emit('new_publication', str(publication)) event.
    """
    try:
        # Controls publications count to reset the view by emit socketio event.
        if client_consumer.publications_count() > client_consumer.max_size:
            emit('reset_data')

        # Get data to consume from client_consumer.
        publication = client_consumer.consume_publication()

        # Send new publication to front-end client by emit sockeio event.
        if publication is not None:
            emit('new_publication', str(publication))
    except Exception as e:
        print('Oopss!', e)


@bp.route('/')
@bp.route('/index')
def index():
    """
    GET route to request the client front end page.

    Returns:
        Response: Render a template with the client front end page.
    """
    return render_template('index.html.j2', title='BYNE Test - Client')


@bp.route('/history', methods=['GET'])
def history():
    """
    Http GET route to request the publications history by calling a service
    get_history() method.

    Returns:
        Response: Render a template with the result of the request.
    """
    try:
        with rpc_proxy() as service4:
            history = service4.get_history()
            return render_template('history.html.j2',
                                   title='BYNE Test - History Result', history=history)
    except Exception as e:
        flash(f'Ooops! {e}', category='error')
    return render_template('history.html.j2',
                           title='BYNE Test - History Result')
