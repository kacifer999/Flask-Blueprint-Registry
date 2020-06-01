from api import serve_app
from flask import Flask
from gevent.pywsgi import WSGIServer


app = serve_app()
server = WSGIServer(('0.0.0.0', 5000), application=app).serve_forever()