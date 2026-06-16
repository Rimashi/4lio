from app.extensions import db


class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=False)

    # Связь с пользователями
    users = db.relationship('User', back_populates='role', lazy='select')

    def __repr__(self):
        return f'<Role {self.name}>'