from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app.extensions import db
from app.services.book_service import BookService
from app.services.review_service import ReviewService

reviews_bp = Blueprint('reviews', __name__)

@reviews_bp.route('/write/<int:book_id>', methods=['GET'])
@login_required
def write_review(book_id):
    book = BookService.get_book(book_id)
    # Проверяем, не писал ли пользователь уже рецензию
    existing = ReviewService.get_user_review(book_id, current_user.id)
    if existing:
        flash('Вы уже оставили рецензию на эту книгу', 'warning')
        return redirect(url_for('books.book', book_id=book_id))
    return render_template('reviews/write_review.html', book=book)

@reviews_bp.route('/submit/<int:book_id>', methods=['POST'])
@login_required
def submit_review(book_id):
    book = BookService.get_book(book_id)
    rating = request.form.get('rating', type=int)
    text = request.form.get('text', '').strip()

    if rating is None or rating < 0 or rating > 5:
        flash('Некорректная оценка', 'danger')
        return redirect(url_for('reviews.write_review', book_id=book_id))
    if not text:
        flash('Текст рецензии не может быть пустым', 'danger')
        return redirect(url_for('reviews.write_review', book_id=book_id))

    try:
        review = ReviewService.create_review(book_id, current_user.id, rating, text)
        flash('Рецензия отправлена на модерацию', 'success')
        return redirect(url_for('books.book', book_id=book_id))
    except ValueError as e:
        flash(str(e), 'danger')
        return redirect(url_for('reviews.write_review', book_id=book_id))
    except Exception:
        db.session.rollback()
        flash('При сохранении рецензии возникла ошибка', 'danger')
        return redirect(url_for('reviews.write_review', book_id=book_id))

@reviews_bp.route('/my')
@login_required
def my_reviews():
    reviews = ReviewService.get_reviews_by_user(current_user.id)
    return render_template('reviews/my_reviews.html', reviews=reviews)