from app import create_app, socket

app = create_app()


@app.shell_context_processor
def make_shell_context():
    """Function to enable testing from python shell interface

    Returns:
        {}
    """
    return {}


if __name__ == '__main__':
    socket.run(app, host='0.0.0.0')
