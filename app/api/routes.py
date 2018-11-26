from . import api
from .resources import *

api.add_resource(ProxyListResource, '/proxy')
api.add_resource(ProxyResource, '/proxy/<int:proxy_id>')

