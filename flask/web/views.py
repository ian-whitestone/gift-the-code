from flask import flash, Blueprint, request, redirect, render_template, url_for, jsonify, Markup, send_from_directory, Response, make_response
from flask.views import MethodView
from flask_login import LoginManager, UserMixin, login_required, current_user
from datetime import datetime, timedelta, date
import time
import json
from werkzeug.exceptions import NotFound
import subprocess
import shlex
import os
from werkzeug.utils import secure_filename

from . import app, allowed_file
# from . import query_db, db
from .login import login_manager # THIS IS NEEDED


SH_data = Blueprint('SH_data', __name__, template_folder='templates')
ROOT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))

class HomePage(MethodView):
    def get(self):
        return render_template('home.html')


class FoodData(MethodView):
    decorators = [login_required]

    def get(self):
        return render_template('food_data.html')

class UploadData(MethodView):
    decorators = [login_required]

    def get(self):
        return render_template('upload_data.html')


SH_data.add_url_rule('/', view_func=HomePage.as_view('home'))
SH_data.add_url_rule('/data/', view_func=FoodData.as_view('FoodData'))
SH_data.add_url_rule('/upload/', view_func=UploadData.as_view('UploadData'))


@app.route('/generate_report/', methods=["POST"])
def generate_report():
    uid = current_user.id


    try:
        # do some stuff
        return jsonify(result='Success')
    except Exception as e:
        flash(Markup("Uh oh! Something went wrong. Please check your inputs again or contact an Admin.<br>"
                     "<b>{error}:</b> {msg}".format(error=type(e).__name__, msg=str(e))), 'danger')
        return jsonify(result='Error')


@app.route('/upload_file', methods=["GET","POST"])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        ff = f.filename
        print 'ff', f.filename

        filename = "{time}_{name}".format(time=datetime.now().strftime("%Y%m%d-%H%M%S"), name=ff)
        print 'filename', filename
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        try:
            f.save(filepath)
            print 'uploaded to', filepath
            return render_template('upload_success.html', ff=ff)
        except:
            flash('Could not upload file', 'danger')
    else:
        return redirect(url_for('SH_data.UploadData'))
