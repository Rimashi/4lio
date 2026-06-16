from datetime import datetime

import bleach
import markdown

from app.extensions import db


class Review(db.Model):
    __tablename__ = 'reviews'
    __table_args__ = (
        db.UniqueConstraint('user_id', 'book_id', name='uq_review_user_book'),
    )

    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id', ondelete='CASCADE'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    status_id = db.Column(db.Integer, db.ForeignKey('review_statuses.id', ondelete='RESTRICT'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)  # 0..5
    text = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # Отношения
    book = db.relationship('Book', back_populates='reviews')
    user = db.relationship('User', back_populates='reviews')
    status = db.relationship('ReviewStatus', back_populates='reviews')

    @property
    def text_html(self):
        """Преобразует Markdown в HTML для отображения."""
        raw = markdown.markdown(self.text, extensions=['nl2br'])
        return bleach.clean(raw, tags=['p','br','strong','em','blockquote','ul','ol','li'], attributes={})

    def __repr__(self):
        return f'<Review {self.id} by {self.user.username}>'