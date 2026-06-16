# app/__init__.py
from flask import Flask

from app.config import Config
from app.extensions import db, login_manager, migrate


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    # Импорт и регистрация blueprints
    from app.controllers.auth import auth_bp
    from app.controllers.books import books_bp
    from app.controllers.collections import collections_bp
    from app.controllers.main import main_bp
    from app.controllers.moderation import moderation_bp
    from app.controllers.profile import profile_bp
    from app.controllers.reviews import reviews_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(books_bp)
    app.register_blueprint(reviews_bp)
    app.register_blueprint(moderation_bp)
    app.register_blueprint(collections_bp)
    app.register_blueprint(profile_bp)

    # Контекстный процессор для current_user
    @app.context_processor
    def inject_user():
        from flask_login import current_user
        return dict(current_user=current_user)

    # Загрузчик пользователя
    from app.models import User
    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    return app