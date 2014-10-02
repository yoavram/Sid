from flask import Flask, request, render_template, send_file
from flask.ext.assets import Environment, Bundle
import os
import csv
import pandas as pd

DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)  
#app.config.from_pyfile('config.py', True)
if app.debug:
	print " * Running in debug mode"

def format_table(table_html):
	print "** formatting table"
	table_html = table_html.replace("<table", "<table class='table'")
	print table_html
	return table_html
app.jinja_env.filters['format_table'] = format_table


@app.route("/")
def index():
	listdir = os.listdir('../images')
	return render_template("index.html", dirs=listdir)

@app.route("/dir/<string:dirname>")
def directory(dirname):
	listdir = os.listdir('../images/' + dirname)
	return render_template("index.html", dirname=dirname, files=listdir)

@app.route("/file/<string:dirname>/<string:fname>")
def file(dirname, fname):
	fullpath = "..\\images\\" + dirname + "\\" + fname
	if fname.endswith('.jpg'):
		return send_file(fullpath, mimetype='image/jpg')
	elif fname.endswith('.png'):
		return send_file(fullpath, mimetype='image/png')
	elif fname.endswith('.csv'):
		data = pd.read_csv(fullpath, index_col="id")			
		return render_template("index.html", table=data)

if __name__ == '__main__':
	# Bind to PORT if defined, otherwise default to 5000.
	port = int(os.environ.get('PORT', 5000))
	app.run(host='127.0.0.1', port=port, debug=app.debug)
