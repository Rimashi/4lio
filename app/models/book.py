import bleach
import markdown

from app.extensions import db

# Вспомогательная таблица для связи книги и жанров
book_genres = db.Table('book_genres',
    db.Column('book_id', db.Integer, db.ForeignKey('books.id', ondelete='CASCADE'), primary_key=True),
    db.Column('genre_id', db.Integer, db.ForeignKey('genres.id', ondelete='CASCADE'), primary_key=True)
)

class Book(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256), nullable=False)
    description = db.Column(db.Text, nullable=False)
    year = db.Column(db.SmallInteger, nullable=False)  # год издания
    publisher = db.Column(db.String(128), nullable=False)
    author = db.Column(db.String(128), nullable=False)
    pages = db.Column(db.Integer, nullable=False)
    cover_id = db.Column(db.Integer, db.ForeignKey('covers.id', ondelete='SET NULL'), nullable=True)

    # Отношения
    cover = db.relationship('Cover', back_populates='book', uselist=False)
    genres = db.relationship('Genre', secondary=book_genres, back_populates='books', lazy='subquery')
    reviews = db.relationship('Review', back_populates='book', cascade='all, delete-orphan', lazy='dynamic')
    history = db.relationship('ViewHistory', back_populates='book', cascade='all, delete-orphan', lazy='dynamic')

    @property
    def avg_rating(self):
        """Средняя оценка только по одобренным рецензиям."""
        approved = [r for r in self.reviews if r.status.name == 'Одобрена']
        if not approved:
            return None
        return round(sum(r.rating for r in approved) / len(approved), 1)

    @property
    def reviews_count(self):
        """Количество одобренных рецензий."""
        return sum(1 for r in self.reviews if r.status.name == 'Одобрена')

    @property
    def description_html(self):
        """Преобразует Markdown в HTML с санитайзингом."""
        allowed_tags = [
            'p', 'br', 'strong', 'em', 'del', 'h2', 'h3',
            'ul', 'ol', 'li', 'blockquote', 'a', 'code', 'pre'
        ]
        allowed_attrs = {'a': ['href', 'title']}
        raw = markdown.markdown(self.description, extensions=['nl2br'])
        return bleach.clean(raw, tags=allowed_tags, attributes=allowed_attrs)

    def __repr__(self):
        return f'<Book {self.title}>'