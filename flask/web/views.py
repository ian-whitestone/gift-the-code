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
from . import data_import, import_survey
# from . import map_data
# from . import query_db, db
from .login import login_manager  # THIS IS NEEDED


SH_data = Blueprint('SH_data', __name__, template_folder='templates')
ROOT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))


class HomePage(MethodView):

    def get(self):
        return render_template('home.html')


class FoodData(MethodView):
    decorators = [login_required]

    def get(self, report_id=None):
        if report_id:
            report = "data/{}.html".format(report_id)
        else:
            report = "data/report_full.html"
        url = url_for('static', filename=report)
        return render_template('food_data.html', url=url)


class UploadData(MethodView):
    decorators = [login_required]

    def get(self):
        return render_template('upload_data.html')


class GenerateReport(MethodView):
    decorators = [login_required]

    def get(self):
        return render_template('generate_report.html')


SH_data.add_url_rule('/', view_func=HomePage.as_view('home'))
SH_data.add_url_rule('/data/', view_func=FoodData.as_view('FoodData'))
SH_data.add_url_rule('/data/<report_id>/',
                     view_func=FoodData.as_view('CustomReport'))
SH_data.add_url_rule('/upload/', view_func=UploadData.as_view('UploadData'))
SH_data.add_url_rule('/generate_report/',
                     view_func=GenerateReport.as_view('GenerateReport'))


@app.route('/upload_file/', methods=["GET", "POST"])
@login_required
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        ff = f.filename
        print('ff', f.filename)

        filename = "{time}_{name}".format(
            time=datetime.now().strftime("%Y%m%d-%H%M%S"), name=ff)
        print('filename', filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        try:
            f.save(filepath)
            print('uploaded to', filepath)
            if filename.lower().startswith('data'):
                data_import.main(filepath)
            elif filename.lower().startswith('survey'):
                import_survey.import_data(filepath)
            print('data loaded successfully')
        query = 'SELECT * FROM data'
        title = 'Annual Report'
        output_path = 'web/static/data/report_full.html'
        render_call = "rmarkdown::render(\"report.Rmd\", params=list(query=\"%s\", title=\"%s\"), output_file = \"%s\")" % (
            query, title, output_path)
        subprocess.call(['Rscript', '-e', render_call])
            return render_template('upload_success.html', ff=ff)
        except Exception as e:
            flash(Markup("Uh oh! Something went wrong. Please check your inputs again or contact an Admin.<br>"
                         "<b>{error}:</b> {msg}".format(error=type(e).__name__, msg=str(e))), 'danger')
            return redirect('/')
    else:
        return redirect(url_for('SH_data.UploadData'))
