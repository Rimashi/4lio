from datetime import datetime

from app.extensions import db


class ViewHistory(db.Model):
    __tablename__ = 'view_history'

    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id', ondelete='CASCADE'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='SET NULL'), nullable=True)
    viewed_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # Отношения
    book = db.relationship('Book', back_populates='history')
    user = db.relationship('User', back_populates='history')

    def __repr__(self):
        return f'<ViewHistory {self.id} book={self.book_id} user={self.user_id}>'