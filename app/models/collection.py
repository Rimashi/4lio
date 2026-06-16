from app.extensions import db

# Вспомогательная таблица для связи подборок и книг
collection_books = db.Table('collection_books',
    db.Column('collection_id', db.Integer, db.ForeignKey('collections.id', ondelete='CASCADE'), primary_key=True),
    db.Column('book_id', db.Integer, db.ForeignKey('books.id', ondelete='CASCADE'), primary_key=True)
)

class Collection(db.Model):
    __tablename__ = 'collections'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)

    # Отношения
    user = db.relationship('User', back_populates='collections')
    books = db.relationship('Book', secondary=collection_books, lazy='subquery')

    def __repr__(self):
        return f'<Collection {self.name}>'