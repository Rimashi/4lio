from app.extensions import db


class ReviewStatus(db.Model):
    __tablename__ = 'review_statuses'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False, unique=True)

    # Связь с рецензиями
    reviews = db.relationship('Review', back_populates='status', lazy='dynamic')

    def __repr__(self):
        return f'<ReviewStatus {self.name}>'