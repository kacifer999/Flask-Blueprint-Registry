# Flask-Blueprint-Registry
A danimic API registry project based on Flask, supports for register and remove blueprint at runtime.  
Reuirement:  
```
importlib
flask
flask_restplus
gevent
werkzeug==0.16.0
```
To Start:
```
python run.py
```

API for Regist  demo:  
[POST] http://127.0.0.1:5000/admin/register  
```
{
    "project_id":"demo",
    "sandbox_id":"demo",
    "sandbox_abs_dir":"This currently does noting"
}
```
API for Unregist demo:  
[POST] http://127.0.0.1:5000/admin/unregister  
```
{
    "sandbox_id":"demo"
}
```
Demo's swagger UI:  
http://127.0.0.1:5000/api/demo/demo
