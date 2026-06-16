import csv
from datetime import datetime
from io import StringIO
from itertools import groupby

from flask import Blueprint, Response, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from sqlalchemy import desc, func

from app.extensions import db
from app.models import Book, Collection, Review, ViewHistory
from app.utils.decorators import admin_required

profile_bp = Blueprint("profile", __name__, url_prefix="/profile")


@profile_bp.route('/')
@login_required
def profile():
    reviews_count = current_user.reviews.count()
    collections_count = current_user.collections.count()
    recent_reviews = current_user.reviews.order_by(Review.created_at.desc()).limit(5).all()
    recent_collections = current_user.collections.order_by(Collection.id.desc()).limit(5).all()
    return render_template("profile/profile.html",
                           reviews_count=reviews_count,
                           collections_count=collections_count,
                           recent_reviews=recent_reviews,
                           recent_collections=recent_collections)

@profile_bp.route("/edit", methods=["POST"])
@login_required
def update_profile():
    last_name = request.form.get("last_name", "").strip()
    first_name = request.form.get("first_name", "").strip()
    middle_name = request.form.get("middle_name", "").strip() or None

    if not last_name or not first_name:
        flash("Имя и фамилия обязательны", "danger")
        return redirect(url_for("profile.profile"))

    current_user.last_name = last_name
    current_user.first_name = first_name
    current_user.middle_name = middle_name
    db.session.commit()
    flash("Профиль обновлён", "success")
    return redirect(url_for("profile.profile"))


@profile_bp.route("/password", methods=["POST"])
@login_required
def change_password():
    current_password = request.form.get("current_password", "")
    new_password = request.form.get("new_password", "")
    confirm = request.form.get("confirm_password", "")

    if not current_user.check_password(current_password):
        flash("Текущий пароль введён неверно", "danger")
    elif new_password != confirm:
        flash("Пароли не совпадают", "danger")
    elif len(new_password) < 6:
        flash("Пароль должен содержать минимум 6 символов", "danger")
    else:
        current_user.set_password(new_password)
        db.session.commit()
        flash("Пароль изменён", "success")
    return redirect(url_for("profile.profile"))


@profile_bp.route('/history')
@login_required
def history():
    records = ViewHistory.query.filter_by(user_id=current_user.id).order_by(ViewHistory.viewed_at.desc()).all()
    # Группируем по дате в Python
    grouped = []
    for date_str, group in groupby(records, key=lambda r: r.viewed_at.strftime('%d.%m.%Y')):
        grouped.append({
            'date': date_str,
            'records': list(group)
        })
    return render_template("profile/history.html", grouped=grouped)


@profile_bp.route("/history/clear", methods=["POST"])
@login_required
def clear_history():
    ViewHistory.query.filter_by(user_id=current_user.id).delete()
    db.session.commit()
    flash("История просмотров очищена", "success")
    return redirect(url_for("profile.history"))


# ===== Статистика (только админ) =====
@profile_bp.route("/stats")
@admin_required
def stats():
    page = request.args.get("page", 1, type=int)
    tab = request.args.get("tab", "log")
    date_from = request.args.get("date_from")
    date_to = request.args.get("date_to")

    # Журнал просмотров
    log_query = ViewHistory.query.order_by(ViewHistory.viewed_at.desc())
    log_pagination = log_query.paginate(page=page, per_page=10, error_out=False)

    # Статистика просмотров (только авторизованные)
    views_query = (
        db.session.query(Book, func.count(ViewHistory.id).label("views"))
        .join(ViewHistory, ViewHistory.book_id == Book.id)
        .filter(ViewHistory.user_id.isnot(None))
        .group_by(Book.id)
    )
    if date_from:
        views_query = views_query.filter(ViewHistory.viewed_at >= date_from)
    if date_to:
        views_query = views_query.filter(ViewHistory.viewed_at <= date_to + " 23:59:59")
    views_pagination = views_query.order_by(desc(func.count(ViewHistory.id))).paginate(page=page, per_page=10, error_out=False)

    # Максимальное количество просмотров для шкалы
    max_views = 0
    views_data = []
    for book, views in views_pagination.items:
        views_data.append((book, views))
        if views > max_views:
            max_views = views

    return render_template(
        "stats.html",
        tab=tab,
        log_pagination=log_pagination,
        views_pagination=views_pagination,
        views_data=views_data,
        max_views=max_views,
        date_from=date_from,
        date_to=date_to,
    )


# Экспорт CSV
@profile_bp.route("/stats/export_log")
@admin_required
def export_log_csv():
    records = ViewHistory.query.order_by(ViewHistory.viewed_at.desc()).all()
    si = StringIO()
    writer = csv.writer(si, delimiter=";")
    writer.writerow(["№", "Пользователь", "Книга", "Дата и время"])
    for idx, rec in enumerate(records, 1):
        user_name = rec.user.full_name if rec.user else "Неаутентифицированный"
        writer.writerow([idx, user_name, rec.book.title, rec.viewed_at.strftime("%d.%m.%Y %H:%M")])
    output = si.getvalue()
    filename = f"journal_{datetime.now().strftime('%Y%m%d')}.csv"
    return Response(output, mimetype="text/csv", headers={"Content-Disposition": f"attachment; filename={filename}"})


@profile_bp.route("/stats/export_views")
@admin_required
def export_views_csv():
    # Экспортируем все просмотры (без пагинации)
    views_query = (
        db.session.query(Book, db.func.count(ViewHistory.id).label("views"))
        .join(ViewHistory, ViewHistory.book_id == Book.id)
        .filter(ViewHistory.user_id.isnot(None))
        .group_by(Book.id)
        .order_by(db.text("views DESC"))
    )
    si = StringIO()
    writer = csv.writer(si, delimiter=";")
    writer.writerow(["№", "Книга", "Просмотры"])
    for idx, (book, views) in enumerate(views_query.all(), 1):
        writer.writerow([idx, book.title, views])
    output = si.getvalue()
    filename = f"views_{datetime.now().strftime('%Y%m%d')}.csv"
    return Response(output, mimetype="text/csv", headers={"Content-Disposition": f"attachment; filename={filename}"})
