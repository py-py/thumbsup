from flask import redirect, url_for

from . import app


@app.route('/')
def index():
    return redirect(url_for('proxy.index'))

