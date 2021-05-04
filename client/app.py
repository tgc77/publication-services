from app import create_app, socket

""""Flask main app startup"""

app = create_app()

if __name__ == '__main__':
    """"Socket to listening incoming data from Redis Queue"""
    socket.run(app, host='0.0.0.0')
