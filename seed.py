import random
from datetime import datetime

from app import create_app
from app.extensions import db
from app.models import Book, Collection, Genre, Review, ReviewStatus, Role, User

app = create_app()

def seed():
    with app.app_context():
        print("Заполнение начальных данных...")

        # 1. Роли
        roles_data = [
            ('Администратор', 'Полный доступ к системе'),
            ('Модератор', 'Может редактировать книги и модерировать рецензии'),
            ('Пользователь', 'Может оставлять рецензии')
        ]
        for name, desc in roles_data:
            if not Role.query.filter_by(name=name).first():
                db.session.add(Role(name=name, description=desc))
        db.session.commit()
        print("Роли созданы.")

        # 2. Статусы рецензий
        statuses = ['На рассмотрении', 'Одобрена', 'Отклонена']
        for s in statuses:
            if not ReviewStatus.query.filter_by(name=s).first():
                db.session.add(ReviewStatus(name=s))
        db.session.commit()
        print("Статусы рецензий созданы.")

        # 3. Жанры
        genres_list = [
            'Роман', 'Фантастика', 'Мистика', 'Детектив',
            'Классика', 'Антиутопия', 'Фэнтези', 'Философия', 'Приключения'
        ]
        for g in genres_list:
            if not Genre.query.filter_by(name=g).first():
                db.session.add(Genre(name=g))
        db.session.commit()
        print("Жанры созданы.")

        # 4. Тестовые пользователи
        admin_role = Role.query.filter_by(name='Администратор').first()
        mod_role = Role.query.filter_by(name='Модератор').first()
        user_role = Role.query.filter_by(name='Пользователь').first()

        users = [
            {'username': 'admin', 'password': 'admin123', 'last_name': 'Администратор', 'first_name': 'Админ', 'role': admin_role},
            {'username': 'moderator', 'password': 'moder123', 'last_name': 'Модератор', 'first_name': 'Мод', 'role': mod_role},
            {'username': 'ivanov', 'password': 'user123', 'last_name': 'Иванов', 'first_name': 'Иван', 'middle_name': 'Иванович', 'role': user_role},
            {'username': 'petrov', 'password': 'user123', 'last_name': 'Петров', 'first_name': 'Пётр', 'middle_name': 'Петрович', 'role': user_role},
            {'username': 'sidorova', 'password': 'user123', 'last_name': 'Сидорова', 'first_name': 'Анна', 'middle_name': 'Сергеевна', 'role': user_role},
        ]
        for u in users:
            if not User.query.filter_by(username=u['username']).first():
                user = User(
                    username=u['username'],
                    last_name=u['last_name'],
                    first_name=u['first_name'],
                    middle_name=u.get('middle_name'),
                    role=u['role']
                )
                user.set_password(u['password'])
                db.session.add(user)
        db.session.commit()
        print("Пользователи созданы.")

        # 5. Тестовые книги
        # Получаем жанры для привязки
        genres = {g.name: g for g in Genre.query.all()}

        books_data = [
            {
                'title': 'Мастер и Маргарита',
                'description': 'Роман Михаила Булгакова, в котором переплетаются мистика, любовь и сатира на советское общество.',
                'year': 1967,
                'publisher': 'Москва журнал',
                'author': 'Михаил Булгаков',
                'pages': 480,
                'genres': ['Роман', 'Мистика']
            },
            {
                'title': '1984',
                'description': 'Культовая антиутопия Джорджа Оруэлла о тоталитарном обществе, где правят ложь и слежка.',
                'year': 1949,
                'publisher': 'Secker & Warburg',
                'author': 'Джордж Оруэлл',
                'pages': 328,
                'genres': ['Антиутопия']
            },
            {
                'title': 'Властелин колец',
                'description': 'Эпическая фэнтези-трилогия Дж. Р. Р. Толкина о противостоянии добра и зла в Средиземье.',
                'year': 1954,
                'publisher': 'Allen & Unwin',
                'author': 'Дж. Р. Р. Толкин',
                'pages': 1200,
                'genres': ['Фэнтези', 'Приключения']
            },
            {
                'title': 'Преступление и наказание',
                'description': 'Социально-психологический роман Фёдора Достоевского о теории "сверхчеловека" и её последствиях.',
                'year': 1866,
                'publisher': 'Русский вестник',
                'author': 'Фёдор Достоевский',
                'pages': 671,
                'genres': ['Классика', 'Роман']
            },
            {
                'title': 'Солярис',
                'description': 'Философская фантастика Станислава Лема о контакте с внеземным разумом.',
                'year': 1961,
                'publisher': 'Wydawnictwo Literackie',
                'author': 'Станислав Лем',
                'pages': 220,
                'genres': ['Фантастика', 'Философия']
            },
            {
                'title': 'Убийство в "Восточном экспрессе"',
                'description': 'Классический детектив Агаты Кристи с Эркюлем Пуаро, расследующим убийство в поезде.',
                'year': 1934,
                'publisher': 'Collins Crime Club',
                'author': 'Агата Кристи',
                'pages': 256,
                'genres': ['Детектив']
            },
        ]

        for data in books_data:
            # Проверяем, есть ли уже такая книга (по названию)
            if Book.query.filter_by(title=data['title']).first():
                continue
            book = Book(
                title=data['title'],
                description=data['description'],
                year=data['year'],
                publisher=data['publisher'],
                author=data['author'],
                pages=data['pages']
            )
            book.genres = [genres[g] for g in data['genres'] if g in genres]
            db.session.add(book)
        db.session.commit()
        print("Книги созданы.")

        # 6. Тестовые рецензии (для пользователей, кроме админа и модератора)
        pending_status = ReviewStatus.query.filter_by(name='На рассмотрении').first()
        approved_status = ReviewStatus.query.filter_by(name='Одобрена').first()
        # Получаем книги
        books = Book.query.all()
        users_for_reviews = User.query.filter(User.role_id == user_role.id).all()
        review_texts = [
            'Отличная книга, рекомендую!',
            'Очень понравилась, читал на одном дыхании.',
            'Интересный сюжет, но немного затянуто.',
            'Классика на все времена, должно быть в каждой библиотеке.',
            'Неожиданный финал, захватывает с первых страниц.',
            'Глубокая философская мысль, заставляет задуматься.',
        ]
        # Для каждой книги добавим 2-3 рецензии
        for book in books[:5]:
            num_reviews = random.randint(2, 3)
            selected_users = random.sample(users_for_reviews, min(num_reviews, len(users_for_reviews)))
            for user in selected_users:
                if not Review.query.filter_by(book_id=book.id, user_id=user.id).first():
                    rating = random.randint(3, 5)
                    status = random.choice([pending_status, approved_status, approved_status, approved_status])  # чаще одобрены
                    review = Review(
                        book_id=book.id,
                        user_id=user.id,
                        rating=rating,
                        text=random.choice(review_texts),
                        status=status,
                        created_at=datetime.utcnow()
                    )
                    db.session.add(review)
        db.session.commit()
        print("Рецензии созданы.")

        # 7. Тестовые подборки для пользователей
        for user in users_for_reviews[:2]:
            col1 = Collection.query.filter_by(name='Любимые книги', user_id=user.id).first()
            if not col1:
                col1 = Collection(name='Любимые книги', user_id=user.id)
                db.session.add(col1)
            col2 = Collection.query.filter_by(name='Хочу прочитать', user_id=user.id).first()
            if not col2:
                col2 = Collection(name='Хочу прочитать', user_id=user.id)
                db.session.add(col2)
            # Добавим книги в подборки
            for book in Book.query.limit(3).all():
                if book not in col1.books:
                    col1.books.append(book)
        db.session.commit()
        print("Подборки созданы.")

        print("Заполнение данными завершено!")

if __name__ == '__main__':
    seed()