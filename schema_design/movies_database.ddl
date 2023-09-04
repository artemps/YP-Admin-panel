CREATE SCHEMA IF NOT EXISTS content;

-- FILM_WORK
CREATE TABLE IF NOT EXISTS content.film_work (
    id uuid PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    creation_date DATE NOT NULL,
    rating FLOAT,
    type VARCHAR(2) NOT NULL,
    created timestamp with time zone,
    modified timestamp with time zone
);
CREATE INDEX film_work_creation_date_rating_idx ON content.film_work(creation_date, rating);
CREATE UNIQUE INDEX film_work_title_idx ON content.film_work(title);

-- PERSON
CREATE TABLE IF NOT EXISTS content.person (
    id uuid PRIMARY KEY,
    full_name VARCHAR(255) NOT NULL,
    created timestamp with time zone,
    modified timestamp with time zone
);
CREATE INDEX person_full_name_idx ON content.person(full_name);
CREATE TABLE IF NOT EXISTS content.person_film_work (
    id uuid PRIMARY KEY,
    film_work_id uuid NOT NULL,
    person_id uuid NOT NULL,
    role VARCHAR(2) NOT NULL,
    created timestamp with time zone
);
CREATE UNIQUE INDEX film_work_person_idx ON content.person_film_work(film_work_id, person_id);

-- GENRE
CREATE TABLE IF NOT EXISTS content.genre (
    id uuid PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    created timestamp with time zone,
    modified timestamp with time zone
);
CREATE TABLE IF NOT EXISTS content.genre_film_work (
    id uuid PRIMARY KEY,
    film_work_id uuid NOT NULL,
    genre_id uuid NOT NULL,
    created timestamp with time zone
);
CREATE UNIQUE INDEX film_work_genre_idx ON content.genre_film_work(film_work_id, genre_id);
