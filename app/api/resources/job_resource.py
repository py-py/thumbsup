from flask_restful import Resource, abort, reqparse

from app import db
from app.models import Proxy, Job

__all__ = ('JobListResource',)


def get_or_abort_if_proxy_doesnt_exist(proxy_id):
    proxy = Proxy.query.filter_by(id=proxy_id).first()
    if not proxy:
        abort(404, message="Proxy id:{} doesn't exist".format(proxy_id))
    return proxy


def generate_job_dict(job):
    return {
        'url': job.url,
        'like': job.like,
        'period': job.period,
        'date': int(job.date.timestamp() * 1000),
        'status': job.status
    }


parser = reqparse.RequestParser(bundle_errors=True)
parser.add_argument('url', type=str, required=True, help='Url cannot be converted.')
parser.add_argument('like', type=int, required=True, help='Like cannot be converted.')
parser.add_argument('period', type=int, required=True, help='Period cannot be converted.')


class JobListResource(Resource):
    def get(self):
        response = [generate_job_dict(job) for job in Job.query.all()]
        return response, 200

    def post(self):
        args = parser.parse_args()
        url = args['url']
        like = args['like']
        period = args['period']

        job = Job(url=url, like=like, period=period)
        db.session.add(job)
        db.session.commit()
        return generate_job_dict(job), 201
