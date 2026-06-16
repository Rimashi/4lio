from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app.extensions import db
from app.models import Book, Collection

collections_bp = Blueprint('collections', __name__, url_prefix='/collections')

@collections_bp.route('/')
@login_required
def my_collections():
    collections = Collection.query.filter_by(user_id=current_user.id).order_by(Collection.id.desc()).all()
    return render_template('collections/my_collections.html', collections=collections)

@collections_bp.route('/create', methods=['POST'])
@login_required
def create_collection():
    name = request.form.get('name', '').strip()
    if not name:
        flash('Введите название подборки', 'danger')
        return redirect(url_for('collections.my_collections'))

    # Проверка на дублирование имени (опционально)
    existing = Collection.query.filter_by(user_id=current_user.id, name=name).first()
    if existing:
        flash('Подборка с таким именем уже существует', 'warning')
        return redirect(url_for('collections.my_collections'))

    collection = Collection(name=name, user_id=current_user.id)
    db.session.add(collection)
    db.session.commit()
    flash(f'Подборка «{name}» создана', 'success')
    return redirect(url_for('collections.my_collections'))

@collections_bp.route('/<int:col_id>')
@login_required
def collection(col_id):
    collection = Collection.query.get_or_404(col_id)
    if collection.user_id != current_user.id:
        abort(403)
    return render_template('collections/collection.html', collection=collection)

@collections_bp.route('/<int:col_id>/delete', methods=['POST'])
@login_required
def delete_collection(col_id):
    collection = Collection.query.get_or_404(col_id)
    if collection.user_id != current_user.id:
        abort(403)
    name = collection.name
    db.session.delete(collection)
    db.session.commit()
    flash(f'Подборка «{name}» удалена', 'success')
    return redirect(url_for('collections.my_collections'))

@collections_bp.route('/add_book', methods=['POST'])
@login_required
def add_book_to_collection():
    book_id = request.form.get('book_id', type=int)
    collection_id = request.form.get('collection_id', type=int)
    if not book_id or not collection_id:
        flash('Не указаны данные', 'danger')
        return redirect(url_for('main.index'))

    collection = Collection.query.get_or_404(collection_id)
    if collection.user_id != current_user.id:
        abort(403)
    book = Book.query.get_or_404(book_id)
    if book not in collection.books:
        collection.books.append(book)
        db.session.commit()
        flash(f'Книга добавлена в подборку «{collection.name}»', 'success')
    else:
        flash('Книга уже есть в подборке', 'info')
    return redirect(url_for('books.book', book_id=book_id))

@collections_bp.route('/<int:col_id>/remove_book/<int:book_id>', methods=['POST'])
@login_required
def remove_book_from_collection(col_id, book_id):
    collection = Collection.query.get_or_404(col_id)
    if collection.user_id != current_user.id:
        abort(403)
    book = Book.query.get_or_404(book_id)
    if book in collection.books:
        collection.books.remove(book)
        db.session.commit()
        flash('Книга удалена из подборки', 'success')
    return redirect(url_for('collections.collection', col_id=col_id))