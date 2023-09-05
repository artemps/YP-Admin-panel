import datetime
import inspect
import uuid
from abc import ABC
from dataclasses import dataclass, field
from typing import ClassVar


@dataclass
class AbstractDataclass(ABC):
    table_name: ClassVar[str] = None

    def __new__(cls, *args, **kwargs):
        if cls == AbstractDataclass:
            raise TypeError("Cannot instantiate abstract class.")
        return super().__new__(cls)

    @classmethod
    def from_dict(cls, fields):
        return cls(**{
            k: v for k, v in fields.items()
            if k in inspect.signature(cls).parameters
        })


@dataclass
class FilmWorkRelation:
    id: uuid.UUID
    film_work_id: uuid.UUID


@dataclass
class FilmWork(AbstractDataclass):
    title: str
    description: str
    creation_date: datetime
    type: str
    rating: float = field(default=0.0)
    created: str = field(default='NOW()')
    modified: str = field(default='NOW()')
    id: uuid.UUID = field(default_factory=uuid.uuid4)

    table_name: ClassVar[str] = 'film_work'


@dataclass
class Genre(AbstractDataclass):
    name: str
    description: str
    created: str = field(default='NOW()')
    modified: str = field(default='NOW()')
    id: uuid.UUID = field(default_factory=uuid.uuid4)

    table_name: ClassVar[str] = 'genre'


@dataclass
class Person(AbstractDataclass):
    full_name: str
    created: str = field(default='NOW()')
    modified: str = field(default='NOW()')
    id: uuid.UUID = field(default_factory=uuid.uuid4)

    table_name: ClassVar[str] = 'person'


@dataclass
class GenreFilmWork(AbstractDataclass, FilmWorkRelation):
    genre_id: uuid.UUID
    created: str = field(default='NOW()')

    table_name: ClassVar[str] = 'genre_film_work'


@dataclass
class PersonFilmWork(AbstractDataclass, FilmWorkRelation):
    person_id: uuid.UUID
    role: str
    created: str = field(default='NOW()')

    table_name: ClassVar[str] = 'person_film_work'

