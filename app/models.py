from datetime import datetime

from flask_login import UserMixin
from sqlalchemy import UniqueConstraint
from sqlalchemy.sql import ClauseElement
from werkzeug.security import generate_password_hash, check_password_hash

from . import db, login


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __str__(self):
        return '<User {}>'.format(self.username)


class Proxy(db.Model):
    __tablename__ = 'proxies'
    id = db.Column(db.Integer, primary_key=True)
    host = db.Column(db.String(15), index=True, nullable=False)
    port = db.Column(db.SmallInteger, nullable=False)
    count_used = db.Column(db.Integer, default=0)

    __table_args__ = (
        UniqueConstraint('host', 'port', name='_host_port_uc'),
    )


class Job(db.Model):
    __tablename__ = 'jobs'
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(512), index=True, nullable=False)
    like = db.Column(db.SmallInteger)
    date = db.Column(db.DateTime, default=datetime.now())
    period = db.Column(db.Integer, default=60*60)
    status = db.Column(db.Boolean, default=False)


def get_or_create(model, defaults=None, **kwargs):
    instance = model.query.filter_by(**kwargs).first()
    if instance:
        return instance, False
    else:
        params = dict((k, v) for k, v in kwargs.items() if not isinstance(v, ClauseElement))
        params.update(defaults or {})
        instance = model(**params)
        db.session.add(instance)
        db.session.commit()
        return instance, True
