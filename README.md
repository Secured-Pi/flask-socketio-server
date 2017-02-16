# flask-socketio-server
Flask server for handling RPi locks' SocketIO connection.
It also handles detecting a face, taking pictures, and sending to the main
Django server.

To use:
First, install OpenCV, then clone this repo and cd into the project directory

```
python3 -m venv ENV
source ENV/bin/activate
pip install -r requirements.txt
./server.py
```

