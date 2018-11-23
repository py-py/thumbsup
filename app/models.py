from flask_login import UserMixin
from sqlalchemy import UniqueConstraint
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login


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


class ProxyHost(db.Model):
    __tablename__ = 'proxies'
    id = db.Column(db.Integer, primary_key=True)
    host = db.Column(db.String(15), index=True, nullable=False)
    port = db.Column(db.SmallInteger, nullable=False)

    __table_args__ = (
        UniqueConstraint('host', 'port', name='_host_port_uc'),
    )
