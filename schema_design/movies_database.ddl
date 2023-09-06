CREATE SCHEMA IF NOT EXISTS content;

-- FILM_WORK
CREATE TABLE IF NOT EXISTS content.film_work (
    id uuid PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    creation_date DATE,
    rating FLOAT,
    type VARCHAR(7) NOT NULL,
    created timestamp with time zone,
    modified timestamp with time zone
);
CREATE INDEX film_work_title_idx ON content.film_work(title);
CREATE INDEX film_work_creation_date_rating_idx ON content.film_work(creation_date, rating);

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
    role VARCHAR(8) NOT NULL,
    created timestamp with time zone
);
ALTER TABLE content.person_film_work ADD CONSTRAINT person_film_work_film_work_id_fk
    FOREIGN KEY (film_work_id) REFERENCES content.film_work (id) ON DELETE CASCADE;
ALTER TABLE content.person_film_work ADD CONSTRAINT person_film_work_person_id_fk
    FOREIGN KEY (person_id) REFERENCES content.person (id) ON DELETE CASCADE;
CREATE UNIQUE INDEX film_work_person_role_unique_idx ON content.person_film_work(film_work_id, person_id, role);
ALTER TABLE content.person_film_work ADD CONSTRAINT film_work_person_role_unique_idx
    UNIQUE USING INDEX film_work_person_role_unique_idx;

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
ALTER TABLE content.genre_film_work ADD CONSTRAINT genre_film_work_film_work_id_fk
    FOREIGN KEY (film_work_id) REFERENCES content.film_work (id) ON DELETE CASCADE;
ALTER TABLE content.genre_film_work ADD CONSTRAINT genre_film_work_genre_id_fk
    FOREIGN KEY (genre_id) REFERENCES content.genre (id) ON DELETE CASCADE;
CREATE UNIQUE INDEX film_work_genre_unique_idx ON content.genre_film_work(film_work_id, genre_id);
ALTER TABLE content.genre_film_work ADD CONSTRAINT film_work_genre_unique_idx
    UNIQUE USING INDEX film_work_genre_unique_idx;
