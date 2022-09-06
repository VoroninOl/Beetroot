from app import app, socketio

if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=8000, debug=True)
    socketio.run(app, allow_unsafe_werkzeug=True)
