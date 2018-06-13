from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask import url_for

db = SQLAlchemy()

class Base(db.Model):
    __abstract__ = True
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class User(Base, UserMixin):
    __tablename__ = 'user'

    ROLE_USER = 10
    ROLE_STAFF = 20
    ROLE_ADMIN = 30

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True, index=True, nullable=False)
    email = db.Column(db.String(64), unique=True, index=True, nullable=False)
    _password = db.Column('password', db.String(256), nullable=False)
    role = db.Column(db.SmallInteger, default=ROLE_USER)
    job = db.Column(db.String(64))

    def __repr__(self):
        return '<User:{}>'.format(self.username)

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, orig_password):
        self._password = generate_password_hash(orig_password)

    def check_password(self, password):
        return check_password_hash(self._password, password)

    @property
    def is_admin(self):
        return self.role == self.ROLE_ADMIN

    @property
    def is_staff(self):
        return self.role == self.ROLE_STAFF

class Env(Base):
    __tablename__ = 'env'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True, index=True, nullable=False)
    person_in_charge_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='SET NULL'))
    person_in_charge = db.relationship('User', uselist=False)
    # Enverment description
    description = db.Column(db.String(256))
    # module databases
    mdbs = db.relationship('Mdb')

    @property
    def url(self):
        return url_for('env.detail', env_id=self.id)

    def __repr__(self):
        return '<Env:{}>'.format(self.name)


class Mdb(Base):
    __tablename__ = 'mdb'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True, index=True)
    mdb_type = db.Column(db.String(128))
    description = db.Column(db.String(256))
    # module database link url
    mdb_url = db.Column(db.String(256))
    mdb_port = db.Column(db.String(128))
    mdb_user = db.Column(db.String(128))
    mdb_psd = db.Column(db.String(128))
    # link to enverment, and delete mdb while enverment deleted
    env_id = db.Column(db.Integer, db.ForeignKey('env.id', ondelete='CASCADE'))
    env = db.relationship('Env', uselist=False)

    @property
    def url(self):
        return url_for('env.mdb', env_id=self.env_id, mdb_id=self.id)

    def __repr__(self):
        return '<Mdb:{}>'.format(self.name)

# using flask-migrate upgrade database
# ```
# export FLASK_APP=manage.py
# flask db migrate -m 'db init'
# flask db upgrade
# ```
