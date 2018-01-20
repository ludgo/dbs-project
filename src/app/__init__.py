import os
from flask import Flask, render_template, url_for
from app.pagination import url_for_other_page
from sqlalchemy import create_engine
from app.properties import *


app = Flask(__name__)

# configure application from file
app.config.from_object('config')

# add custom template engine methods
app.jinja_env.globals['url_for_other_page'] = url_for_other_page

''' START
following 2 methods ensure static css in not cached, thus updated by browser every time it has changed
'''
@app.context_processor
def override_url_for():
	return dict(url_for=dated_url_for)

def dated_url_for(endpoint, **values):
	if endpoint == 'static':
		filename = values.get('filename', None)
		if filename:
			file_path = os.path.join(app.root_path,	endpoint, filename)
			values['q'] = int(os.stat(file_path).st_mtime)
	return url_for(endpoint, **values)
# END

# initialize connection pool engine
DB_URL = 'postgresql://{}:{}@{}:{}/{}'.format(DB_USERNAME, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME)
engine = create_engine(DB_URL, pool_size=10, max_overflow=0)
engine.connect()

# whole app's 404
@app.errorhandler(404)
def not_found(error):
	return render_template('404.html'), 404

# integrate separate blueprints
from app.module_inquiries.controllers import blueprint_inquiries
app.register_blueprint(blueprint_inquiries)

from app.module_api.controllers import blueprint_api
app.register_blueprint(blueprint_api)

