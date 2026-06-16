from app.extensions import db


class Cover(db.Model):
    __tablename__ = 'covers'

    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(256), nullable=False)
    mime_type = db.Column(db.String(64), nullable=False)
    md5_hash = db.Column(db.String(32), nullable=False, unique=True)

    # Обратная связь с книгой (One-to-One)
    book = db.relationship('Book', back_populates='cover', uselist=False)

    def __repr__(self):
        return f'<Cover {self.filename}>'