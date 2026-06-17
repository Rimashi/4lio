import os

from flask import Blueprint, current_app, flash, jsonify, redirect, render_template, request, url_for
from flask_login import current_user

from app.extensions import db
from app.models import Book, Cover, Genre
from app.models.view_history import ViewHistory
from app.utils.decorators import admin_required, moderator_required
from app.utils.helpers import save_cover

books_bp = Blueprint('books', __name__, url_prefix='/books')

@books_bp.route('/<int:book_id>')
def book(book_id):
    book = Book.query.get_or_404(book_id)
    # Запись просмотра
    user_id = current_user.id if current_user.is_authenticated else None
    if user_id:
        from datetime import datetime
        today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        count = ViewHistory.query.filter(
            ViewHistory.book_id == book.id,
            ViewHistory.user_id == user_id,
            ViewHistory.viewed_at >= today_start
        ).count()
        if count < 10:
            db.session.add(ViewHistory(book_id=book.id, user_id=user_id))
            db.session.commit()
    else:
        db.session.add(ViewHistory(book_id=book_id, user_id=None))
        db.session.commit()

    # Рецензия текущего пользователя
    user_review = None
    if current_user.is_authenticated:
        from app.models import Review
        user_review = Review.query.filter_by(book_id=book_id, user_id=current_user.id).first()

    from app.models import ReviewStatus
    approved_status = ReviewStatus.query.filter_by(name='Одобрена').first()
    reviews = book.reviews.filter_by(status=approved_status).all()

    collections = []
    if current_user.is_authenticated:
        from app.models import Collection
        collections = Collection.query.filter_by(user_id=current_user.id).all()

    return render_template(
        'books/book.html',
        book=book,
        user_review=user_review,
        reviews=reviews,
        collections=collections
    )

@books_bp.route('/add', methods=['GET', 'POST'])
@admin_required
def book_add():
    genres = Genre.query.order_by(Genre.name).all()

    if request.method == 'POST':
        try:
            title = request.form.get('title', '').strip()
            description = request.form.get('description', '').strip()
            year = int(request.form.get('year', 0))
            publisher = request.form.get('publisher', '').strip()
            author = request.form.get('author', '').strip()
            pages = int(request.form.get('pages', 0))

            print("request.files keys:", list(request.files.keys()))
            print("cover filename:", request.files.get('cover').filename if 'cover' in request.files else 'NO FILE')

            if not all([title, description, publisher, author]) or year < 1000 or pages < 1:
                raise ValueError('Некорректные данные')

            cover = None
            if 'cover' in request.files and request.files['cover'].filename:
                cover = save_cover(request.files['cover'])
                if cover is None:
                    flash('Недопустимый формат обложки', 'danger')
                    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                        return jsonify(error='Недопустимый формат обложки'), 400
                    return render_template('books/book_form.html', genres=genres, book=None)

            book = Book(
                title=title, description=description, year=year,
                publisher=publisher, author=author, pages=pages,
                cover=cover
            )
            selected_genres = request.form.getlist('genres')
            if selected_genres:
                book.genres = Genre.query.filter(Genre.id.in_(selected_genres)).all()

            db.session.add(book)
            db.session.commit()

            flash(f'Книга «{book.title}» успешно добавлена', 'success')
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify(redirect=url_for('books.book', book_id=book.id))
            return redirect(url_for('books.book', book_id=book.id))

        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f'Ошибка при добавлении книги: {e}')
            flash('При сохранении данных возникла ошибка. Проверьте корректность введённых данных.', 'danger')
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify(error='При сохранении данных возникла ошибка. Проверьте корректность введённых данных.'), 400

    return render_template('books/book_form.html', genres=genres, book=None)

@books_bp.route('/<int:book_id>/edit', methods=['GET', 'POST'])
@moderator_required
def book_edit(book_id):
    book = Book.query.get_or_404(book_id)
    genres = Genre.query.order_by(Genre.name).all()

    if request.method == 'POST':
        try:
            book.title = request.form.get('title', '').strip()
            book.description = request.form.get('description', '').strip()
            book.year = int(request.form.get('year', 0))
            book.publisher = request.form.get('publisher', '').strip()
            book.author = request.form.get('author', '').strip()
            book.pages = int(request.form.get('pages', 0))

            if not all([book.title, book.description, book.publisher, book.author]) or book.year < 1000 or book.pages < 1:
                raise ValueError('Некорректные данные')

            selected_genres = request.form.getlist('genres')
            if selected_genres:
                book.genres = Genre.query.filter(Genre.id.in_(selected_genres)).all()
            else:
                book.genres = []

            if 'cover' in request.files and request.files['cover'].filename:
                cover = save_cover(request.files['cover'])
                if cover:
                    book.cover = cover

            db.session.commit()
            flash(f'Книга «{book.title}» успешно обновлена', 'success')
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify(redirect=url_for('books.book', book_id=book.id))
            return redirect(url_for('books.book', book_id=book.id))

        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f'Ошибка при редактировании книги: {e}')
            flash('При сохранении данных возникла ошибка. Проверьте корректность введённых данных.', 'danger')
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify(error='При сохранении данных возникла ошибка. Проверьте корректность введённых данных.'), 400

    return render_template('books/book_form.html', genres=genres, book=book)

@books_bp.route('/<int:book_id>/delete', methods=['POST'])
@admin_required
def book_delete(book_id):
    book = Book.query.get_or_404(book_id)
    title = book.title

    if book.cover:
        other = Book.query.filter(Book.cover_id == book.cover_id, Book.id != book_id).first()
        if not other:
            path = os.path.join(current_app.config['UPLOAD_FOLDER'], book.cover.filename)
            if os.path.exists(path):
                os.remove(path)

    db.session.delete(book)
    db.session.commit()
    flash(f'Книга «{title}» удалена', 'success')
    return redirect(url_for('main.index'))