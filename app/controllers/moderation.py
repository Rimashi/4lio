from flask import Blueprint, flash, redirect, render_template, request, url_for

from app.extensions import db
from app.models import Review, ReviewStatus
from app.utils.decorators import moderator_required

moderation_bp = Blueprint('moderation', __name__, url_prefix='/moderation')

@moderation_bp.route('/')
@moderator_required
def moderation():
    page = request.args.get('page', 1, type=int)
    pending_status = ReviewStatus.query.filter_by(name='На рассмотрении').first()
    if not pending_status:
        flash('Статус "На рассмотрении" не найден', 'danger')
        return render_template('moderation/moderation.html', reviews=[], pagination=None)

    pagination = (
        Review.query
        .filter_by(status=pending_status)
        .order_by(Review.created_at.asc())
        .paginate(page=page, per_page=10, error_out=False)
    )
    return render_template('moderation/moderation.html', reviews=pagination.items, pagination=pagination)

@moderation_bp.route('/<int:review_id>')
@moderator_required
def moderation_review(review_id):
    review = Review.query.get_or_404(review_id)
    return render_template('moderation/moderation_review.html', review=review)

@moderation_bp.route('/<int:review_id>/approve', methods=['POST'])
@moderator_required
def review_approve(review_id):
    review = Review.query.get_or_404(review_id)
    approved_status = ReviewStatus.query.filter_by(name='Одобрена').first()
    if not approved_status:
        flash('Статус "Одобрена" не найден', 'danger')
        return redirect(url_for('moderation.moderation'))
    review.status = approved_status
    db.session.commit()
    flash('Рецензия одобрена', 'success')
    return redirect(url_for('moderation.moderation'))

@moderation_bp.route('/<int:review_id>/reject', methods=['POST'])
@moderator_required
def review_reject(review_id):
    review = Review.query.get_or_404(review_id)
    rejected_status = ReviewStatus.query.filter_by(name='Отклонена').first()
    if not rejected_status:
        flash('Статус "Отклонена" не найден', 'danger')
        return redirect(url_for('moderation.moderation'))
    review.status = rejected_status
    db.session.commit()
    flash('Рецензия отклонена', 'danger')
    return redirect(url_for('moderation.moderation'))