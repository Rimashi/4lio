-- ================================================
-- folio — schema.sql (PostgreSQL)
-- psql -U postgres -d folio -f schema.sql
-- или сразу создать БД:
-- createdb folio && psql -U postgres -d folio -f schema.sql
-- ================================================

-- Роли пользователей
CREATE TABLE IF NOT EXISTS roles (
    id          SERIAL PRIMARY KEY,
    name        VARCHAR(64) NOT NULL UNIQUE,
    description TEXT        NOT NULL
);

-- Пользователи
CREATE TABLE IF NOT EXISTS users (
    id            SERIAL PRIMARY KEY,
    username      VARCHAR(64)  NOT NULL UNIQUE,
    password_hash VARCHAR(256) NOT NULL,
    last_name     VARCHAR(64)  NOT NULL,
    first_name    VARCHAR(64)  NOT NULL,
    middle_name   VARCHAR(64),
    role_id       INTEGER NOT NULL REFERENCES roles(id)
);

-- Жанры
CREATE TABLE IF NOT EXISTS genres (
    id   SERIAL PRIMARY KEY,
    name VARCHAR(64) NOT NULL UNIQUE
);

-- Обложки
CREATE TABLE IF NOT EXISTS covers (
    id        SERIAL PRIMARY KEY,
    filename  VARCHAR(256) NOT NULL,
    mime_type VARCHAR(64)  NOT NULL,
    md5_hash  VARCHAR(32)  NOT NULL UNIQUE
);

-- Книги
CREATE TABLE IF NOT EXISTS books (
    id          SERIAL PRIMARY KEY,
    title       VARCHAR(256) NOT NULL,
    description TEXT         NOT NULL,
    year        SMALLINT     NOT NULL,
    publisher   VARCHAR(128) NOT NULL,
    author      VARCHAR(128) NOT NULL,
    pages       INTEGER      NOT NULL,
    cover_id    INTEGER REFERENCES covers(id)
);

-- Книги <-> Жанры (many-to-many)
CREATE TABLE IF NOT EXISTS book_genres (
    book_id  INTEGER NOT NULL REFERENCES books(id)  ON DELETE CASCADE,
    genre_id INTEGER NOT NULL REFERENCES genres(id) ON DELETE CASCADE,
    PRIMARY KEY (book_id, genre_id)
);

-- Статусы рецензий
CREATE TABLE IF NOT EXISTS review_statuses (
    id   SERIAL PRIMARY KEY,
    name VARCHAR(32) NOT NULL UNIQUE
);

-- Рецензии
CREATE TABLE IF NOT EXISTS reviews (
    id         SERIAL PRIMARY KEY,
    book_id    INTEGER NOT NULL REFERENCES books(id)           ON DELETE CASCADE,
    user_id    INTEGER NOT NULL REFERENCES users(id)           ON DELETE CASCADE,
    status_id  INTEGER NOT NULL REFERENCES review_statuses(id),
    rating     INTEGER NOT NULL CHECK (rating BETWEEN 0 AND 5),
    text       TEXT    NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    UNIQUE (user_id, book_id)
);

-- Подборки
CREATE TABLE IF NOT EXISTS collections (
    id      SERIAL PRIMARY KEY,
    name    VARCHAR(128) NOT NULL,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE
);

-- Подборки <-> Книги (many-to-many)
CREATE TABLE IF NOT EXISTS collection_books (
    collection_id INTEGER NOT NULL REFERENCES collections(id) ON DELETE CASCADE,
    book_id       INTEGER NOT NULL REFERENCES books(id)       ON DELETE CASCADE,
    PRIMARY KEY (collection_id, book_id)
);

-- История просмотров
CREATE TABLE IF NOT EXISTS view_history (
    id        SERIAL PRIMARY KEY,
    book_id   INTEGER NOT NULL REFERENCES books(id) ON DELETE CASCADE,
    user_id   INTEGER REFERENCES users(id) ON DELETE SET NULL,
    viewed_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- ================================================
-- Начальные данные
-- ================================================

INSERT INTO roles (name, description) VALUES
    ('Администратор', 'Суперпользователь: полный доступ, создание и удаление книг'),
    ('Модератор',     'Редактирование книг и модерация рецензий'),
    ('Пользователь',  'Просмотр книг и написание рецензий')
ON CONFLICT (name) DO NOTHING;

INSERT INTO review_statuses (name) VALUES
    ('На рассмотрении'), ('Одобрена'), ('Отклонена')
ON CONFLICT (name) DO NOTHING;

INSERT INTO genres (name) VALUES
    ('Роман'), ('Фантастика'), ('Мистика'), ('Детектив'),
    ('Классика'), ('Антиутопия'), ('Фэнтези'), ('Философия'), ('Приключения')
ON CONFLICT (name) DO NOTHING;