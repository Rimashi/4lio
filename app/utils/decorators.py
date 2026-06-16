from functools import wraps

from flask import flash, redirect, request, url_for
from flask_login import current_user


def login_required_message(f):
    """Декоратор, перенаправляющий на страницу входа с сообщением."""
    @wraps(f)
    def decorated(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('Для выполнения данного действия необходимо пройти процедуру аутентификации', 'warning')
            return redirect(url_for('auth.login', next=request.url))
        return f(*args, **kwargs)
    return decorated

def admin_required(f):
    """Декоратор, разрешающий доступ только администраторам."""
    @wraps(f)
    def decorated(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('Для выполнения данного действия необходимо пройти процедуру аутентификации', 'warning')
            return redirect(url_for('auth.login', next=request.url))
        if not current_user.is_admin():
            flash('У вас недостаточно прав для выполнения данного действия', 'danger')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated

def moderator_required(f):
    """Декоратор, разрешающий доступ модераторам и администраторам."""
    @wraps(f)
    def decorated(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('Для выполнения данного действия необходимо пройти процедуру аутентификации', 'warning')
            return redirect(url_for('auth.login', next=request.url))
        if not current_user.is_moderator():
            flash('У вас недостаточно прав для выполнения данного действия', 'danger')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated