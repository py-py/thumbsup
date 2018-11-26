from app import app, db
from app.models import User, Proxy, Job


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Proxy': Proxy, 'Job': Job}
