from app import app, db
from app.models import User, Proxy, Job
from sqlalchemy.exc import IntegrityError


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Proxy': Proxy, 'Job': Job}


@app.cli.command(short_help='Create superuser for application.')
def create_superuser():
    import os
    from dotenv import load_dotenv

    load_dotenv()
    username = os.getenv('SUPERUSER_NAME')
    email = os.getenv('SUPERUSER_EMAIL')
    password = os.getenv('SUPERUSER_PASSWORD')

    u = User(username=username, email=email, is_superuser=True)
    u.set_password(password)
    db.session.add(u)

    try:
        db.session.commit()
    except IntegrityError:
        print('User with email:"{}" or username:"{}" was added before.'.format(email, username))
    else:
        print('SUCCESS: Superuser added.')


@app.cli.command(short_help='Download proxies in database from API.')
def download_proxies():
    from app.tasks import download_proxy
    download_proxy.delay()
    print('SUCCESS: Proxies are downloaded.')


@app.cli.command(short_help='Cache user agents in "/tmp" folder.')
def cache_useragent():
    from fake_useragent import UserAgent, FakeUserAgentError
    try:
        UserAgent()
    except FakeUserAgentError:
        pass
    else:
        print('SUCCESS: Fake UserAgents is cached.')
