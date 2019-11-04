from api import serve_app
from flask import Flask
from gevent.pywsgi import WSGIServer
print('Api Start Loading.')
app = serve_app()
print('Api Start Serving.')
WSGIServer(('0.0.0.0', 5000), application=app).serve_forever()