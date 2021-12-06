# for local run -> $export FLASK_APP=services/web/flask_app/app.py
# $flask run -h 0.0.0.0
from . import create_app

app = create_app()
