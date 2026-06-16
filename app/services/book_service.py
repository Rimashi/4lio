import os

from flask import current_app
from sqlalchemy import desc, func

from app.extensions import db
from app.models.book import Book
from app.models.genre import Genre
from app.models.view_history import ViewHistory
from app.utils.helpers import save_cover


class BookService:
    @staticmethod
    def get_paginated_books(page=1, per_page=10, filters=None):
        """Возвращает пагинированный список книг с фильтрацией."""
        query = Book.query.order_by(Book.year.desc())
        if filters:
            if filters.get('title'):
                query = query.filter(Book.title.ilike(f"%{filters['title']}%"))
            if filters.get('author'):
                query = query.filter(Book.author.ilike(f"%{filters['author']}%"))
            if filters.get('genre'):
                query = query.filter(Book.genres.any(Genre.id == filters['genre']))
            if filters.get('year'):
                query = query.filter(Book.year == filters['year'])
            if filters.get('pages_from'):
                query = query.filter(Book.pages >= filters['pages_from'])
            if filters.get('pages_to'):
                query = query.filter(Book.pages <= filters['pages_to'])
        return query.paginate(page=page, per_page=per_page, error_out=False)

    @staticmethod
    def get_book(book_id: int) -> Book:
        return Book.query.get_or_404(book_id)

    @staticmethod
    def create_book(data: dict, cover_file=None) -> Book:
        """Создаёт новую книгу."""
        cover = None
        if cover_file:
            cover = save_cover(cover_file)
            if cover is None:
                raise ValueError('Недопустимый формат обложки')

        book = Book(
            title=data['title'],
            description=data['description'],
            year=data['year'],
            publisher=data['publisher'],
            author=data['author'],
            pages=data['pages'],
            cover=cover
        )
        if data.get('genres'):
            book.genres = Genre.query.filter(Genre.id.in_(data['genres'])).all()

        db.session.add(book)
        db.session.commit()
        return book

    @staticmethod
    def update_book(book: Book, data: dict, cover_file=None) -> Book:
        """Обновляет данные книги."""
        book.title = data['title']
        book.description = data['description']
        book.year = data['year']
        book.publisher = data['publisher']
        book.author = data['author']
        book.pages = data['pages']

        if 'genres' in data and data['genres'] is not None:
            book.genres = Genre.query.filter(Genre.id.in_(data['genres'])).all()

        if cover_file:
            cover = save_cover(cover_file)
            if cover:
                book.cover = cover

        db.session.commit()
        return book

    @staticmethod
    def delete_book(book: Book) -> None:
        """Удаляет книгу и связанный файл обложки, если он не используется."""
        if book.cover:
            # Проверяем, есть ли другие книги с этой же обложкой
            other = Book.query.filter(
                Book.cover_id == book.cover_id,
                Book.id != book.id
            ).first()
            if not other:
                path = os.path.join(current_app.config['UPLOAD_FOLDER'], book.cover.filename)
                if os.path.exists(path):
                    os.remove(path)

        db.session.delete(book)
        db.session.commit()

    @staticmethod
    def get_popular_books(limit=5, days=90):
        from datetime import datetime, timedelta
        cutoff = datetime.utcnow() - timedelta(days=days)
        return (
            db.session.query(Book, func.count(ViewHistory.id).label('views'))
            .join(ViewHistory, ViewHistory.book_id == Book.id)
            .filter(ViewHistory.viewed_at >= cutoff)
            .group_by(Book.id)
            .order_by(desc(func.count(ViewHistory.id)))
            .limit(limit)
            .all()
        )

    @staticmethod
    def get_recently_viewed(user_id: int, limit=5):
        """Возвращает недавно просмотренные книги пользователя."""
        records = (
            ViewHistory.query
            .filter_by(user_id=user_id)
            .order_by(ViewHistory.viewed_at.desc())
            .limit(limit)
            .all()
        )
        return [r.book for r in records]

    @staticmethod
    def get_genres():
        return Genre.query.order_by(Genre.name).all()

    @staticmethod
    def get_years():
        years = db.session.query(Book.year).distinct().order_by(Book.year.desc()).all()
        return [y[0] for y in years]