from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_user, logout_user

from app.extensions import db
from app.models import User

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        remember = bool(request.form.get('remember'))

        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user, remember=remember)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('main.index'))
        flash('Невозможно аутентифицироваться с указанными логином и паролем', 'danger')

    return render_template('auth/login.html')

@auth_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@auth_bp.route('/register', methods=['POST'])
def register():
    # Регистрация через отдельную форму (у нас регистрация на той же странице)
    if request.method == 'POST':
        last_name = request.form.get('last_name', '').strip()
        first_name = request.form.get('first_name', '').strip()
        middle_name = request.form.get('middle_name', '').strip() or None
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        password_confirm = request.form.get('password_confirm', '')

        if not all([last_name, first_name, username, password]):
            flash('Все обязательные поля должны быть заполнены', 'danger')
            return redirect(url_for('auth.login'))

        if password != password_confirm:
            flash('Пароли не совпадают', 'danger')
            return redirect(url_for('auth.login'))

        if len(password) < 6:
            flash('Пароль должен содержать минимум 6 символов', 'danger')
            return redirect(url_for('auth.login'))

        if User.query.filter_by(username=username).first():
            flash('Пользователь с таким логином уже существует', 'danger')
            return redirect(url_for('auth.login'))

        # Назначаем роль "Пользователь" (id=3, предполагаем, что она есть)
        from app.models import Role
        user_role = Role.query.filter_by(name='Пользователь').first()
        if not user_role:
            flash('Системная ошибка: роль не найдена', 'danger')
            return redirect(url_for('auth.login'))

        user = User(
            username=username,
            last_name=last_name,
            first_name=first_name,
            middle_name=middle_name,
            role=user_role
        )
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        flash('Регистрация успешна! Теперь вы можете войти.', 'success')
        return redirect(url_for('auth.login'))

    return redirect(url_for('auth.login'))