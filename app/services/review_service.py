from app.extensions import db
from app.models.review import Review
from app.models.review_status import ReviewStatus


class ReviewService:
    @staticmethod
    def get_review(review_id: int) -> Review:
        return Review.query.get_or_404(review_id)

    @staticmethod
    def create_review(book_id: int, user_id: int, rating: int, text: str) -> Review:
        """Создаёт рецензию со статусом 'На рассмотрении'."""
        # Проверяем, не писал ли пользователь уже рецензию на эту книгу
        existing = Review.query.filter_by(book_id=book_id, user_id=user_id).first()
        if existing:
            raise ValueError('Вы уже оставили рецензию на эту книгу')

        status = ReviewStatus.query.filter_by(name='На рассмотрении').first()
        if not status:
            raise ValueError('Статус "На рассмотрении" не найден')

        review = Review(
            book_id=book_id,
            user_id=user_id,
            rating=rating,
            text=text,
            status=status
        )
        db.session.add(review)
        db.session.commit()
        return review

    @staticmethod
    def approve_review(review: Review) -> None:
        status = ReviewStatus.query.filter_by(name='Одобрена').first()
        if not status:
            raise ValueError('Статус "Одобрена" не найден')
        review.status = status
        db.session.commit()

    @staticmethod
    def reject_review(review: Review) -> None:
        status = ReviewStatus.query.filter_by(name='Отклонена').first()
        if not status:
            raise ValueError('Статус "Отклонена" не найден')
        review.status = status
        db.session.commit()

    @staticmethod
    def get_pending_reviews(page=1, per_page=10):
        """Возвращает пагинированный список рецензий на рассмотрении."""
        status = ReviewStatus.query.filter_by(name='На рассмотрении').first()
        if not status:
            return None
        return (
            Review.query
            .filter_by(status_id=status.id)
            .order_by(Review.created_at.asc())
            .paginate(page=page, per_page=per_page, error_out=False)
        )

    @staticmethod
    def get_reviews_by_user(user_id: int):
        return (
            Review.query
            .filter_by(user_id=user_id)
            .order_by(Review.created_at.desc())
            .all()
        )

    @staticmethod
    def get_approved_reviews(book_id: int):
        status = ReviewStatus.query.filter_by(name='Одобрена').first()
        if not status:
            return []
        return (
            Review.query
            .filter_by(book_id=book_id, status_id=status.id)
            .order_by(Review.created_at.desc())
            .all()
        )

    @staticmethod
    def get_user_review(book_id: int, user_id: int):
        return Review.query.filter_by(book_id=book_id, user_id=user_id).first()