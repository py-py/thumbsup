from flask import render_template, jsonify, request
from flask_login import login_required

from . import job_bp
from ..models import Job


@job_bp.route('/')
@login_required
def index():
    jobs = Job.query.order_by(Job.date.desc())
    return render_template('job/index.html', title='Jobs', jobs=jobs)


@job_bp.route('/proxy')
# @login_required
def get_proxies_job():
    job_id = request.args.get('jobID')
    job = Job.query.get(job_id)
    data = []
    if job:
        for proxy in job.success_used_proxies:
            data.append({
                'host': proxy.host,
                'port': proxy.port,
                'is_success': True,
            })
        for proxy in job.failed_used_proxies:
            data.append({
                'host': proxy.host,
                'port': proxy.port,
                'is_success': False,
            })
    return render_template('job/modal_table.html', data=data)
