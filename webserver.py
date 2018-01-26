#!/usr/bin/env python
import sys
import os
from flask import Flask, Response, make_response, stream_with_context, send_file, request
from functools import wraps, update_wrapper
from datetime import datetime
import cgi
app = Flask('Contributions Viewer')

def nocache(view):
    @wraps(view)
    def no_cache(*args, **kwargs):
        response = make_response(view(*args, **kwargs))
        response.headers['Last-Modified'] = datetime.now()
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '-1'
        return response
    return update_wrapper(no_cache, view)

@app.route('/data/<filename>')
@nocache
def send_data(filename):
    return send_file(os.path.join('data', os.path.basename(filename)), mimetype='application/json')

@app.route('/js/<filename>')
def send_js(filename):
    return send_file(os.path.join('js', os.path.basename(filename)), mimetype="text/js")

@app.route('/css/<filename>')
def send_css(filename):
    return send_file(os.path.join('css', os.path.basename(filename)), mimetype="text/css")


@app.route('/')
def root_page():
    return send_file('index.html', mimetype='text/html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
