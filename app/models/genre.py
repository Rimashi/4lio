from app.extensions import db


class Genre(db.Model):
    __tablename__ = 'genres'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False, unique=True)

    # Обратная связь с книгами (через secondary таблицу book_genres)
    books = db.relationship('Book', secondary='book_genres', back_populates='genres', lazy='dynamic')

    def __repr__(self):
        return f'<Genre {self.name}>'