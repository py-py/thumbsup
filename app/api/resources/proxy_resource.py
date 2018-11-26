from flask_restful import Resource, abort, reqparse

from app import db
from app.models import Proxy

__all__ = ('ProxyResource', 'ProxyListResource',)


def get_or_abort_if_proxy_doesnt_exist(proxy_id):
    proxy = Proxy.query.filter_by(id=proxy_id).first()
    if not proxy:
        abort(404, message="Proxy id:{} doesn't exist".format(proxy_id))
    return proxy


def generate_proxy_dict(proxy):
    return {
        'host': proxy.host,
        'port': proxy.port,
    }


parser = reqparse.RequestParser(bundle_errors=True)
parser.add_argument('host', type=str, required=True, help='Host cannot be converted.')
parser.add_argument('port', type=int, required=True, help='Port cannot be converted.')


class ProxyListResource(Resource):
    def get(self):
        response = [generate_proxy_dict(proxy) for proxy in Proxy.query.all()]
        return response, 200

    def post(self):
        args = parser.parse_args()
        host = args['host']
        port = args['port']

        proxy_exist = Proxy.query.filter_by(host=host, port=port).first()
        if not proxy_exist:
            proxy = Proxy(host=host, port=port)
            db.session.add(proxy)
            db.session.commit()
        else:
            proxy = proxy_exist
        return generate_proxy_dict(proxy), 201


class ProxyResource(Resource):
    def get(self, proxy_id):
        proxy = get_or_abort_if_proxy_doesnt_exist(proxy_id)
        return generate_proxy_dict(proxy)

    def delete(self, proxy_id):
        proxy = get_or_abort_if_proxy_doesnt_exist(proxy_id)
        db.session.delete(proxy)
        db.session.commit()
        return '', 204

    def put(self, proxy_id):
        proxy = get_or_abort_if_proxy_doesnt_exist(proxy_id)
        args = parser.parse_args()
        host = args['host']
        port = args['port']

        proxy_exist = Proxy.query.filter_by(host=host, port=port).first()
        if not proxy_exist:
            proxy.host = host
            proxy.port = port
            db.session.add(proxy)
            db.session.commit()
        else:
            proxy = proxy_exist
        return generate_proxy_dict(proxy), 201
