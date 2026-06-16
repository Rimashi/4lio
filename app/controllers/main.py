from datetime import datetime, timedelta

from flask import Blueprint, render_template, request
from flask_login import current_user
from sqlalchemy import desc, func

from app.extensions import db
from app.models import Book, Genre, ViewHistory

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    title = request.args.get('title', '').strip()
    author = request.args.get('author', '').strip()
    genre = request.args.get('genre', type=int)
    year = request.args.get('year', type=int)
    pages_from = request.args.get('pages_from', type=int)
    pages_to = request.args.get('pages_to', type=int)

    query = Book.query.order_by(Book.year.desc())

    if title:
        query = query.filter(Book.title.ilike(f'%{title}%'))
    if author:
        query = query.filter(Book.author.ilike(f'%{author}%'))
    if genre:
        query = query.filter(Book.genres.any(Genre.id == genre))
    if year:
        query = query.filter(Book.year == year)
    if pages_from:
        query = query.filter(Book.pages >= pages_from)
    if pages_to:
        query = query.filter(Book.pages <= pages_to)

    pagination = query.paginate(page=page, per_page=10, error_out=False)

    # Популярные (топ 5 за 3 месяца)
    three_months_ago = datetime.utcnow() - timedelta(days=90)
    # views = db.func.count(ViewHistory.id).label('views')
    popular = (
        db.session.query(Book, func.count(ViewHistory.id).label('views'))
        .join(ViewHistory, ViewHistory.book_id == Book.id)
        .filter(ViewHistory.viewed_at >= three_months_ago)
        .group_by(Book.id)
        .order_by(desc(func.count(ViewHistory.id)))
        .limit(5)
        .all()
    )
    # Недавно просмотренные (для авторизованных)
    recently = []
    if current_user.is_authenticated:
        recently = (
            ViewHistory.query
            .filter_by(user_id=current_user.id)
            .order_by(ViewHistory.viewed_at.desc())
            .limit(5)
            .all()
        )

    genres_all = Genre.query.order_by(Genre.name).all()
    years_all = db.session.query(Book.year).distinct().order_by(Book.year.desc()).all()

    filters = {
        'title': title,
        'author': author,
        'genre': genre,
        'year': year,
        'pages_from': pages_from,
        'pages_to': pages_to,
    }

    return render_template(
        'books/index.html',
        books=pagination.items,
        pagination=pagination,
        popular=popular,
        recently=recently,
        genres=genres_all,
        years=[y[0] for y in years_all],
        filters=filters
    )