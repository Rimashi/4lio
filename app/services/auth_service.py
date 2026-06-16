from app.extensions import db
from app.models.role import Role
from app.models.user import User


class AuthService:
    @staticmethod
    def authenticate(username: str, password: str) -> User | None:
        """Проверяет логин и пароль, возвращает пользователя или None."""
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            return user
        return None

    @staticmethod
    def register_user(data: dict) -> User:
        """
        Регистрирует нового пользователя.
        data: dict с полями username, password, last_name, first_name, middle_name (опционально)
        """
        # Проверяем, что пользователь не существует
        if User.query.filter_by(username=data['username']).first():
            raise ValueError('Пользователь с таким логином уже существует')

        # Получаем роль "Пользователь" (по умолчанию)
        role = Role.query.filter_by(name='Пользователь').first()
        if not role:
            raise ValueError('Роль "Пользователь" не найдена. Сначала добавьте роли.')

        user = User(
            username=data['username'],
            last_name=data['last_name'],
            first_name=data['first_name'],
            middle_name=data.get('middle_name'),
            role=role
        )
        user.set_password(data['password'])
        db.session.add(user)
        db.session.commit()
        return user

    @staticmethod
    def get_user_by_id(user_id: int) -> User | None:
        return db.session.get(User, user_id)

    @staticmethod
    def update_profile(user: User, data: dict) -> User:
        """Обновляет профиль пользователя."""
        user.last_name = data['last_name']
        user.first_name = data['first_name']
        user.middle_name = data.get('middle_name')
        db.session.commit()
        return user

    @staticmethod
    def change_password(user: User, current_password: str, new_password: str) -> bool:
        """Меняет пароль, если текущий верен."""
        if not user.check_password(current_password):
            return False
        user.set_password(new_password)
        db.session.commit()
        return True