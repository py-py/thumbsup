from datetime import datetime
from random import choice

from flask_login import UserMixin
from sqlalchemy import UniqueConstraint
from sqlalchemy.sql import ClauseElement
from werkzeug.security import generate_password_hash, check_password_hash

from . import db, login


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


proxies = db.Table(
    'proxies',
    db.Column('job_id', db.Integer, db.ForeignKey('job.id'), primary_key=True),
    db.Column('proxy_id', db.Integer, db.ForeignKey('proxy.id'), primary_key=True),
    db.Column('is_success', db.Boolean)
)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    is_superuser = db.Column(db.Boolean, default=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __str__(self):
        return '<User {}>'.format(self.username)


class Proxy(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    host = db.Column(db.String(15), index=True, nullable=False)
    port = db.Column(db.Integer, nullable=False)
    count_used = db.Column(db.Integer, default=0)

    __table_args__ = (
        UniqueConstraint('host', 'port', name='_host_port_uc'),
    )

    @property
    def union(self):
        return '{host}:{port}'.format(host=self.host, port=self.port)

    def __repr__(self):
        return '{class_name}({host}:{port})'.format(class_name=self.__class__.__name__, host=self.host, port=self.port)


class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(512), index=True, nullable=False)
    date = db.Column(db.DateTime, default=datetime.now())
    period = db.Column(db.Integer, default=60 * 60)

    ordered_likes = db.Column(db.SmallInteger)
    added_likes = db.Column(db.SmallInteger, default=0)

    proxies = db.relationship('Proxy', secondary=proxies, lazy='subquery', backref=db.backref('jobs', lazy=True))

    @property
    def status(self):
        return self.added_likes >= self.ordered_likes

    @property
    def free_proxy(self):
        free_proxies = self.free_proxies

        if len(free_proxies):
            return choice(free_proxies)
        raise Exception('Free proxies not exist for current job.')

    @property
    def free_proxies(self):
        proxies_ids = {p.id for p in Proxy.query.all()}
        proxies_obj = {p.id for p in self.proxies}
        not_used_proxies = proxies_ids - proxies_obj
        return [Proxy.query.get(i) for i in not_used_proxies]


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
