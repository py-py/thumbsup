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


class Association(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.ForeignKey('job.id'))
    proxy_id = db.Column(db.ForeignKey('proxy.id'))
    is_success = db.Column(db.Boolean, default=False)

    job = db.relationship('Job', backref='associations')
    proxy = db.relationship('Proxy', backref='associations')

    __table_args__ = (
        UniqueConstraint('job_id', 'proxy_id'),
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
        UniqueConstraint('host', 'port'),
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

    proxies = db.relationship('Proxy',
                              secondary=Association.__table__,
                              primaryjoin="Job.id==Association.job_id",
                              backref="jobs")
    @property
    def added_likes(self):
        return len([a for a in self.associations if a.is_success])

    @property
    def status(self):
        return self.added_likes >= self.ordered_likes

    def get_free_proxy(self):
        free_proxies = self.get_free_proxies()

        if len(free_proxies):
            return choice(free_proxies)
        raise Exception('Free proxies not exist for current job.')

    def get_free_proxies(self):
        proxies_ids = {p.id for p in Proxy.query.all()}
        proxies_obj = {p.id for p in self.proxies}
        not_used_proxies = proxies_ids - proxies_obj
        return [Proxy.query.get(i) for i in not_used_proxies]

    @property
    def success_used_proxies(self):
        return [Proxy.query.get(a.proxy_id) for a in self.associations if a.is_success]

    @property
    def failed_used_proxies(self):
        return [Proxy.query.get(a.proxy_id) for a in self.associations if not a.is_success]


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
