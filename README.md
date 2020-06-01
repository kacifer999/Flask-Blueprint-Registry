# Flask-Blueprint-Registry
A danimic API registry project based on Flask, supports for register and remove blueprint at runtime.

To Start:
pip install reuirement.txt
python run.py

API for Regist and Unregist demo:

[POST] http://127.0.0.1:5000/admin/register 

{
    "project_id":"demo",
    "sandbox_id":"demo",
    "sandbox_abs_dir":""
}

[POST] http://127.0.0.1:5000/admin/unregister 

{
    "sandbox_id":"demo"
}

Demo's swagger UI:
http://127.0.0.1:5000/api/demo/demo
