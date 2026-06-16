from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from app.extensions import db


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), nullable=False, unique=True)
    password_hash = db.Column(db.String(256), nullable=False)
    last_name = db.Column(db.String(64), nullable=False)
    first_name = db.Column(db.String(64), nullable=False)
    middle_name = db.Column(db.String(64), nullable=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id', ondelete='RESTRICT'), nullable=False)

    # Отношения
    role = db.relationship('Role', back_populates='users', lazy='joined')
    reviews = db.relationship('Review', back_populates='user', cascade='all, delete-orphan', lazy='dynamic')
    collections = db.relationship('Collection', back_populates='user', cascade='all, delete-orphan', lazy='dynamic')
    history = db.relationship('ViewHistory', back_populates='user', cascade='all, delete-orphan', lazy='dynamic')

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    @property
    def full_name(self) -> str:
        parts = [self.last_name, self.first_name]
        if self.middle_name:
            parts.append(self.middle_name)
        return ' '.join(parts)

    @property
    def short_name(self) -> str:
        """Иванов И. И."""
        s = self.last_name
        if self.first_name:
            s += f' {self.first_name[0]}.'
        if self.middle_name:
            s += f' {self.middle_name[0]}.'
        return s

    def is_admin(self) -> bool:
        return self.role.name == 'Администратор'

    def is_moderator(self) -> bool:
        return self.role.name in ('Администратор', 'Модератор')

    def __repr__(self):
        return f'<User {self.username}>'