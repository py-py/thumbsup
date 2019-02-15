from . import api
from .resources import *

api.add_resource(ProxyListResource,     '/proxy',                   endpoint='proxies')
api.add_resource(ProxyResource,         '/proxy/<int:proxy_id>',    endpoint='proxy')

api.add_resource(JobListResource,       '/job',                     endpoint='jobs')
