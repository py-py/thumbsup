from flask import render_template
from flask_login import login_required

from . import job_bp
from ..models import Job


@job_bp.route('/')
@login_required
def index():
    jobs = Job.query.order_by(Job.date.desc())
    return render_template('job/index.html', title='Jobs', jobs=jobs)
