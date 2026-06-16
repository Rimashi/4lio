import hashlib
import os
from datetime import datetime

from flask import current_app
from flask_login import current_user

from app.extensions import db
from app.models.cover import Cover
from app.models.review_status import ReviewStatus
from app.models.view_history import ViewHistory

ALLOWED_MIME = {'image/jpeg', 'image/png', 'image/webp', 'image/gif'}

def save_cover(file) -> Cover | None:
    """
    Сохраняет файл обложки. Если MD5 уже есть — возвращает существующую запись.
    """
    if not file:
        return None
    data = file.read()
    md5 = hashlib.md5(data).hexdigest()

    # Проверяем, нет ли уже такой обложки
    existing = Cover.query.filter_by(md5_hash=md5).first()
    if existing:
        return existing

    mime = file.mimetype
    if mime not in ALLOWED_MIME:
        return None

    cover = Cover(filename='', mime_type=mime, md5_hash=md5)
    db.session.add(cover)
    db.session.flush()  # получаем id до commit

    # Определяем расширение
    ext = file.filename.rsplit('.', 1)[-1].lower() if '.' in file.filename else 'jpg'
    filename = f'{cover.id}.{ext}'
    cover.filename = filename

    upload_dir = current_app.config['UPLOAD_FOLDER']
    os.makedirs(upload_dir, exist_ok=True)
    with open(os.path.join(upload_dir, filename), 'wb') as f:
        f.write(data)

    db.session.commit()
    return cover

def record_view(book):
    """
    Записывает просмотр книги текущим пользователем.
    Лимит: не более 10 просмотров в день для одного пользователя.
    """
    user_id = current_user.id if current_user.is_authenticated else None

    if user_id:
        today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        count = ViewHistory.query.filter(
            ViewHistory.book_id == book.id,
            ViewHistory.user_id == user_id,
            ViewHistory.viewed_at >= today_start
        ).count()
        if count >= 10:
            return

    db.session.add(ViewHistory(book_id=book.id, user_id=user_id))
    db.session.commit()

def get_pending_status():
    """Возвращает объект статуса 'На рассмотрении'."""
    return ReviewStatus.query.filter_by(name='На рассмотрении').first()

def get_approved_status():
    """Возвращает объект статуса 'Одобрена'."""
    return ReviewStatus.query.filter_by(name='Одобрена').first()

def get_rejected_status():
    """Возвращает объект статуса 'Отклонена'."""
    return ReviewStatus.query.filter_by(name='Отклонена').first()