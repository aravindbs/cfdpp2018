from app import app
import os
from flask import render_template, url_for

@app.route('/')
def index():
    return render_template('index.html', title = "Home")



#######Prevents cacehing of static files in the browser#######
@app.context_processor
#@cross_origin(supports_credentials=True)
def override_url_for():
    return dict(url_for=dated_url_for)


def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                     endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)
##############################################################