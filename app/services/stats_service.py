from datetime import datetime

from sqlalchemy import desc, func

from app.extensions import db
from app.models.book import Book
from app.models.view_history import ViewHistory


class StatsService:
    @staticmethod
    def get_log_paginated(page=1, per_page=10):
        """Возвращает пагинированный журнал просмотров."""
        return (
            ViewHistory.query
            .order_by(ViewHistory.viewed_at.desc())
            .paginate(page=page, per_page=per_page, error_out=False)
        )

    @staticmethod
    def get_views_stats(date_from=None, date_to=None, page=1, per_page=10):
        query = (
            db.session.query(Book, func.count(ViewHistory.id).label('views'))
            .join(ViewHistory, ViewHistory.book_id == Book.id)
            .filter(ViewHistory.user_id.isnot(None))
            .group_by(Book.id)
        )
        if date_from:
            query = query.filter(ViewHistory.viewed_at >= date_from)
        if date_to:
            date_to_end = datetime.combine(date_to, datetime.max.time())
            query = query.filter(ViewHistory.viewed_at <= date_to_end)

        return query.order_by(desc(func.count(ViewHistory.id))).paginate(page=page, per_page=per_page, error_out=False)
    
    @staticmethod
    def get_max_views(date_from=None, date_to=None):
        """Возвращает максимальное количество просмотров для шкалы."""
        query = (
            db.session.query(db.func.count(ViewHistory.id))
            .join(ViewHistory, ViewHistory.book_id == Book.id)
            .filter(ViewHistory.user_id.isnot(None))
        )
        if date_from:
            query = query.filter(ViewHistory.viewed_at >= date_from)
        if date_to:
            date_to_end = datetime.combine(date_to, datetime.max.time())
            query = query.filter(ViewHistory.viewed_at <= date_to_end)

        # Группируем по книгам и берём максимум
        max_views = query.group_by(ViewHistory.book_id).order_by(db.text('count DESC')).limit(1).first()
        return max_views[0] if max_views else 0

    @staticmethod
    def get_csv_log_data():
        """Возвращает все записи журнала для экспорта в CSV."""
        records = ViewHistory.query.order_by(ViewHistory.viewed_at.desc()).all()
        return [
            {
                'id': r.id,
                'user': r.user.full_name if r.user else 'Неаутентифицированный',
                'book': r.book.title,
                'viewed_at': r.viewed_at.strftime('%d.%m.%Y %H:%M')
            }
            for r in records
        ]

    @staticmethod
    def get_csv_views_data(date_from=None, date_to=None):
        """Возвращает все данные статистики просмотров для CSV."""
        query = (
            db.session.query(Book, db.func.count(ViewHistory.id).label('views'))
            .join(ViewHistory, ViewHistory.book_id == Book.id)
            .filter(ViewHistory.user_id.isnot(None))
            .group_by(Book.id)
        )
        if date_from:
            query = query.filter(ViewHistory.viewed_at >= date_from)
        if date_to:
            date_to_end = datetime.combine(date_to, datetime.max.time())
            query = query.filter(ViewHistory.viewed_at <= date_to_end)

        results = query.order_by(db.text('views DESC')).all()
        return [
            {'book': b.title, 'views': views}
            for b, views in results
        ]