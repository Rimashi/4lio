--
-- PostgreSQL database dump
--

\restrict lWIE1RAuYprqAPyA2OR8tFUmgxicDbX7eEjytJ6QTMFYzit0nfRml5DqAuA2Tmz

-- Dumped from database version 18.4
-- Dumped by pg_dump version 18.4

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


--
-- Name: book_genres; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.book_genres (
    book_id integer NOT NULL,
    genre_id integer NOT NULL
);


--
-- Name: books; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.books (
    id integer NOT NULL,
    title character varying(256) NOT NULL,
    description text NOT NULL,
    year smallint NOT NULL,
    publisher character varying(128) NOT NULL,
    author character varying(128) NOT NULL,
    pages integer NOT NULL,
    cover_id integer
);


--
-- Name: books_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.books_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: books_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.books_id_seq OWNED BY public.books.id;


--
-- Name: collection_books; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.collection_books (
    collection_id integer NOT NULL,
    book_id integer NOT NULL
);


--
-- Name: collections; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.collections (
    id integer NOT NULL,
    name character varying(128) NOT NULL,
    user_id integer NOT NULL
);


--
-- Name: collections_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.collections_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: collections_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.collections_id_seq OWNED BY public.collections.id;


--
-- Name: covers; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.covers (
    id integer NOT NULL,
    filename character varying(256) NOT NULL,
    mime_type character varying(64) NOT NULL,
    md5_hash character varying(32) NOT NULL
);


--
-- Name: covers_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.covers_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: covers_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.covers_id_seq OWNED BY public.covers.id;


--
-- Name: genres; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.genres (
    id integer NOT NULL,
    name character varying(64) NOT NULL
);


--
-- Name: genres_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.genres_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: genres_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.genres_id_seq OWNED BY public.genres.id;


--
-- Name: review_statuses; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.review_statuses (
    id integer NOT NULL,
    name character varying(32) NOT NULL
);


--
-- Name: review_statuses_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.review_statuses_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: review_statuses_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.review_statuses_id_seq OWNED BY public.review_statuses.id;


--
-- Name: reviews; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.reviews (
    id integer NOT NULL,
    book_id integer NOT NULL,
    user_id integer NOT NULL,
    status_id integer NOT NULL,
    rating integer NOT NULL,
    text text NOT NULL,
    created_at timestamp without time zone NOT NULL
);


--
-- Name: reviews_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.reviews_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: reviews_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.reviews_id_seq OWNED BY public.reviews.id;


--
-- Name: roles; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.roles (
    id integer NOT NULL,
    name character varying(64) NOT NULL,
    description text NOT NULL
);


--
-- Name: roles_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.roles_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: roles_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.roles_id_seq OWNED BY public.roles.id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.users (
    id integer NOT NULL,
    username character varying(64) NOT NULL,
    password_hash character varying(256) NOT NULL,
    last_name character varying(64) NOT NULL,
    first_name character varying(64) NOT NULL,
    middle_name character varying(64),
    role_id integer NOT NULL
);


--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- Name: view_history; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.view_history (
    id integer NOT NULL,
    book_id integer NOT NULL,
    user_id integer,
    viewed_at timestamp without time zone NOT NULL
);


--
-- Name: view_history_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.view_history_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: view_history_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.view_history_id_seq OWNED BY public.view_history.id;


--
-- Name: books id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.books ALTER COLUMN id SET DEFAULT nextval('public.books_id_seq'::regclass);


--
-- Name: collections id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.collections ALTER COLUMN id SET DEFAULT nextval('public.collections_id_seq'::regclass);


--
-- Name: covers id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.covers ALTER COLUMN id SET DEFAULT nextval('public.covers_id_seq'::regclass);


--
-- Name: genres id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.genres ALTER COLUMN id SET DEFAULT nextval('public.genres_id_seq'::regclass);


--
-- Name: review_statuses id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.review_statuses ALTER COLUMN id SET DEFAULT nextval('public.review_statuses_id_seq'::regclass);


--
-- Name: reviews id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.reviews ALTER COLUMN id SET DEFAULT nextval('public.reviews_id_seq'::regclass);


--
-- Name: roles id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.roles ALTER COLUMN id SET DEFAULT nextval('public.roles_id_seq'::regclass);


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Name: view_history id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.view_history ALTER COLUMN id SET DEFAULT nextval('public.view_history_id_seq'::regclass);


--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.alembic_version (version_num) FROM stdin;
99e2659c10b0
\.


--
-- Data for Name: book_genres; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.book_genres (book_id, genre_id) FROM stdin;
1	1
1	3
2	6
3	7
3	9
4	5
4	1
5	2
5	8
6	4
\.


--
-- Data for Name: books; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.books (id, title, description, year, publisher, author, pages, cover_id) FROM stdin;
1	Мастер и Маргарита	Роман Михаила Булгакова, в котором переплетаются мистика, любовь и сатира на советское общество.	1967	Москва журнал	Михаил Булгаков	480	\N
2	1984	Культовая антиутопия Джорджа Оруэлла о тоталитарном обществе, где правят ложь и слежка.	1949	Secker & Warburg	Джордж Оруэлл	328	\N
3	Властелин колец	Эпическая фэнтези-трилогия Дж. Р. Р. Толкина о противостоянии добра и зла в Средиземье.	1954	Allen & Unwin	Дж. Р. Р. Толкин	1200	\N
4	Преступление и наказание	Социально-психологический роман Фёдора Достоевского о теории "сверхчеловека" и её последствиях.	1866	Русский вестник	Фёдор Достоевский	671	\N
5	Солярис	Философская фантастика Станислава Лема о контакте с внеземным разумом.	1961	Wydawnictwo Literackie	Станислав Лем	220	\N
6	Убийство в "Восточном экспрессе"	Классический детектив Агаты Кристи с Эркюлем Пуаро, расследующим убийство в поезде.	1934	Collins Crime Club	Агата Кристи	256	\N
\.


--
-- Data for Name: collection_books; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.collection_books (collection_id, book_id) FROM stdin;
1	1
1	2
1	3
3	1
3	2
3	3
\.


--
-- Data for Name: collections; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.collections (id, name, user_id) FROM stdin;
1	Любимые книги	3
2	Хочу прочитать	3
3	Любимые книги	4
4	Хочу прочитать	4
\.


--
-- Data for Name: covers; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.covers (id, filename, mime_type, md5_hash) FROM stdin;
\.


--
-- Data for Name: genres; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.genres (id, name) FROM stdin;
1	Роман
2	Фантастика
3	Мистика
4	Детектив
5	Классика
6	Антиутопия
7	Фэнтези
8	Философия
9	Приключения
\.


--
-- Data for Name: review_statuses; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.review_statuses (id, name) FROM stdin;
1	На рассмотрении
2	Одобрена
3	Отклонена
\.


--
-- Data for Name: reviews; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.reviews (id, book_id, user_id, status_id, rating, text, created_at) FROM stdin;
1	1	5	2	4	Глубокая философская мысль, заставляет задуматься.	2026-06-16 19:26:04.606692
2	1	3	2	3	Отличная книга, рекомендую!	2026-06-16 19:26:04.610087
3	1	4	2	3	Глубокая философская мысль, заставляет задуматься.	2026-06-16 19:26:04.611525
4	2	5	2	5	Очень понравилась, читал на одном дыхании.	2026-06-16 19:26:04.613331
5	2	3	1	5	Очень понравилась, читал на одном дыхании.	2026-06-16 19:26:04.614785
6	2	4	2	3	Отличная книга, рекомендую!	2026-06-16 19:26:04.615991
7	3	5	2	5	Очень понравилась, читал на одном дыхании.	2026-06-16 19:26:04.617586
8	3	3	1	5	Неожиданный финал, захватывает с первых страниц.	2026-06-16 19:26:04.618812
9	3	4	2	3	Интересный сюжет, но немного затянуто.	2026-06-16 19:26:04.620129
10	4	5	2	4	Неожиданный финал, захватывает с первых страниц.	2026-06-16 19:26:04.621428
11	4	3	2	3	Очень понравилась, читал на одном дыхании.	2026-06-16 19:26:04.622553
13	5	3	2	4	Интересный сюжет, но немного затянуто.	2026-06-16 19:26:04.624474
14	5	4	2	3	Неожиданный финал, захватывает с первых страниц.	2026-06-16 19:26:04.625436
15	5	6	2	4	test	2026-06-16 20:36:39.317108
12	5	5	3	3	Неожиданный финал, захватывает с первых страниц.	2026-06-16 19:26:04.623532
\.


--
-- Data for Name: roles; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.roles (id, name, description) FROM stdin;
1	Администратор	Полный доступ к системе
2	Модератор	Может редактировать книги и модерировать рецензии
3	Пользователь	Может оставлять рецензии
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.users (id, username, password_hash, last_name, first_name, middle_name, role_id) FROM stdin;
1	admin	scrypt:32768:8:1$HWmUYzldFbS988KL$f1c1f36be637adac4ed22231583e8404592592d4792938f778e289f576171d7ca0eb4ccadacfd6363bc464b38dec020bc9fad74dec167866f04933dffbaa6cab	Администратор	Админ	\N	1
2	moderator	scrypt:32768:8:1$vSbbhJZKGVcQL1FW$1b81a8c487403151d694bb9d3168d88e6223384d82a3744a7ca24e1b4521db53b19d1c6f245dc77ba2d43b5afccd7e81beb9e7e7a376dc3bcaedf21a8d251b08	Модератор	Мод	\N	2
3	ivanov	scrypt:32768:8:1$G8uoAQ3VjhyJZJjz$41bcc1c255439d13cad35f4a94be900ad4a2d61db5629093c0d7128b57a244c8173040cffe0024c257ee29e37d3f6bc475caf2bec504bcae3e4aacdc97b62804	Иванов	Иван	Иванович	3
4	petrov	scrypt:32768:8:1$uqIb58oC53GlzwXz$06dfc99fbe1f997e621f0e70d901637ece5868faa807b01c57870efdb590dc45c5867b8ede9f9dae99bea756c5fc76399497035740e8833d1f2a99dbc0cbc08f	Петров	Пётр	Петрович	3
5	sidorova	scrypt:32768:8:1$rsH0SYqeKPqWZgpA$2cba289867d9163b9a69bde5d3943003591a01105a64a5b7f5553e437b9961cbac18ecd080b31a5dacbf5856c30db0388ca77a16f493b8bcba7d02c985d74c4b	Сидорова	Анна	Сергеевна	3
6	test	scrypt:32768:8:1$jhTkjyqiM21x3irt$5f23e67cb52e37407173a844e344c80dc49e39874bea6bd6fed96a5640a73a1277190c83831f479a7b76fa6b075a3cc18a801a264176a5992480bf7273ada8a9	test	test1	\N	3
\.


--
-- Data for Name: view_history; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.view_history (id, book_id, user_id, viewed_at) FROM stdin;
1	1	\N	2026-06-16 20:20:48.042423
2	5	\N	2026-06-16 20:23:51.875237
3	2	\N	2026-06-16 20:24:09.787664
4	5	6	2026-06-16 20:29:55.296062
5	5	6	2026-06-16 20:31:38.011543
6	5	6	2026-06-16 20:36:31.80541
7	5	6	2026-06-16 20:36:39.328669
8	5	\N	2026-06-16 20:36:57.757364
9	5	6	2026-06-16 20:37:12.605885
10	5	\N	2026-06-16 20:37:26.211438
11	5	6	2026-06-16 20:45:40.717809
12	5	6	2026-06-16 20:49:41.811708
15	5	2	2026-06-16 21:10:42.541403
16	5	2	2026-06-16 21:11:10.230732
\.


--
-- Name: books_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.books_id_seq', 6, true);


--
-- Name: collections_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.collections_id_seq', 4, true);


--
-- Name: covers_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.covers_id_seq', 1, false);


--
-- Name: genres_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.genres_id_seq', 9, true);


--
-- Name: review_statuses_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.review_statuses_id_seq', 3, true);


--
-- Name: reviews_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.reviews_id_seq', 15, true);


--
-- Name: roles_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.roles_id_seq', 3, true);


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.users_id_seq', 6, true);


--
-- Name: view_history_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.view_history_id_seq', 16, true);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: book_genres book_genres_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.book_genres
    ADD CONSTRAINT book_genres_pkey PRIMARY KEY (book_id, genre_id);


--
-- Name: books books_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.books
    ADD CONSTRAINT books_pkey PRIMARY KEY (id);


--
-- Name: collection_books collection_books_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.collection_books
    ADD CONSTRAINT collection_books_pkey PRIMARY KEY (collection_id, book_id);


--
-- Name: collections collections_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.collections
    ADD CONSTRAINT collections_pkey PRIMARY KEY (id);


--
-- Name: covers covers_md5_hash_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.covers
    ADD CONSTRAINT covers_md5_hash_key UNIQUE (md5_hash);


--
-- Name: covers covers_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.covers
    ADD CONSTRAINT covers_pkey PRIMARY KEY (id);


--
-- Name: genres genres_name_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.genres
    ADD CONSTRAINT genres_name_key UNIQUE (name);


--
-- Name: genres genres_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.genres
    ADD CONSTRAINT genres_pkey PRIMARY KEY (id);


--
-- Name: review_statuses review_statuses_name_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.review_statuses
    ADD CONSTRAINT review_statuses_name_key UNIQUE (name);


--
-- Name: review_statuses review_statuses_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.review_statuses
    ADD CONSTRAINT review_statuses_pkey PRIMARY KEY (id);


--
-- Name: reviews reviews_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.reviews
    ADD CONSTRAINT reviews_pkey PRIMARY KEY (id);


--
-- Name: roles roles_name_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.roles
    ADD CONSTRAINT roles_name_key UNIQUE (name);


--
-- Name: roles roles_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.roles
    ADD CONSTRAINT roles_pkey PRIMARY KEY (id);


--
-- Name: reviews uq_review_user_book; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.reviews
    ADD CONSTRAINT uq_review_user_book UNIQUE (user_id, book_id);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: users users_username_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_username_key UNIQUE (username);


--
-- Name: view_history view_history_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.view_history
    ADD CONSTRAINT view_history_pkey PRIMARY KEY (id);


--
-- Name: book_genres book_genres_book_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.book_genres
    ADD CONSTRAINT book_genres_book_id_fkey FOREIGN KEY (book_id) REFERENCES public.books(id) ON DELETE CASCADE;


--
-- Name: book_genres book_genres_genre_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.book_genres
    ADD CONSTRAINT book_genres_genre_id_fkey FOREIGN KEY (genre_id) REFERENCES public.genres(id) ON DELETE CASCADE;


--
-- Name: books books_cover_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.books
    ADD CONSTRAINT books_cover_id_fkey FOREIGN KEY (cover_id) REFERENCES public.covers(id) ON DELETE SET NULL;


--
-- Name: collection_books collection_books_book_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.collection_books
    ADD CONSTRAINT collection_books_book_id_fkey FOREIGN KEY (book_id) REFERENCES public.books(id) ON DELETE CASCADE;


--
-- Name: collection_books collection_books_collection_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.collection_books
    ADD CONSTRAINT collection_books_collection_id_fkey FOREIGN KEY (collection_id) REFERENCES public.collections(id) ON DELETE CASCADE;


--
-- Name: collections collections_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.collections
    ADD CONSTRAINT collections_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: reviews reviews_book_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.reviews
    ADD CONSTRAINT reviews_book_id_fkey FOREIGN KEY (book_id) REFERENCES public.books(id) ON DELETE CASCADE;


--
-- Name: reviews reviews_status_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.reviews
    ADD CONSTRAINT reviews_status_id_fkey FOREIGN KEY (status_id) REFERENCES public.review_statuses(id) ON DELETE RESTRICT;


--
-- Name: reviews reviews_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.reviews
    ADD CONSTRAINT reviews_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: users users_role_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_role_id_fkey FOREIGN KEY (role_id) REFERENCES public.roles(id) ON DELETE RESTRICT;


--
-- Name: view_history view_history_book_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.view_history
    ADD CONSTRAINT view_history_book_id_fkey FOREIGN KEY (book_id) REFERENCES public.books(id) ON DELETE CASCADE;


--
-- Name: view_history view_history_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.view_history
    ADD CONSTRAINT view_history_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE SET NULL;


--
-- PostgreSQL database dump complete
--

\unrestrict lWIE1RAuYprqAPyA2OR8tFUmgxicDbX7eEjytJ6QTMFYzit0nfRml5DqAuA2Tmz

