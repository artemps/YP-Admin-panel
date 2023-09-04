from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from .abstract import TimeStampedMixin, UUIDMixin


class Filmwork(UUIDMixin, TimeStampedMixin):

    class FilmworkType(models.TextChoices):
        MOVIE = 'MV', _('Movie')
        TV_SHOW = 'TV', _('Tv Show')

    title = models.CharField(verbose_name=_('Title'), max_length=255)
    description = models.TextField(verbose_name=_('Description'), blank=True)
    creation_date = models.DateField(verbose_name=_('Release date'))
    rating = models.FloatField(
        verbose_name=_('Rating'),
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    type = models.CharField(
        max_length=2,
        choices=FilmworkType.choices,
        default=FilmworkType.MOVIE,
    )
    genres = models.ManyToManyField('Genre', through='GenreFilmwork')
    persons = models.ManyToManyField('Person', through='PersonFilmwork')

    class Meta:
        db_table = "content\".\"film_work"
        verbose_name = _('Filmwork')
        verbose_name_plural = _('Filmworks')

    def __str__(self):
        return self.title


class Genre(UUIDMixin, TimeStampedMixin):
    name = models.CharField(verbose_name=_('Title'), max_length=255)
    description = models.TextField(verbose_name=_('Description'), blank=True)

    class Meta:
        db_table = "content\".\"genre"
        verbose_name = _('Genre')
        verbose_name_plural = _('Genres')

    def __str__(self):
        return self.name


class Person(UUIDMixin, TimeStampedMixin):
    full_name = models.CharField(verbose_name=_('Name'), max_length=255)

    class Meta:
        db_table = "content\".\"person"
        verbose_name = _('Person')
        verbose_name_plural = _('Persons')

    def __str__(self):
        return self.full_name


class GenreFilmwork(UUIDMixin):
    film_work = models.ForeignKey('Filmwork', on_delete=models.CASCADE)
    genre = models.ForeignKey('Genre', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "content\".\"genre_film_work"


class PersonFilmwork(UUIDMixin):

    class PersonFilmworkRole(models.TextChoices):
        ACTOR = 'AC', _('Actor')
        WRITER = 'WR', _('Writer')
        DIRECTOR = 'DR', _('Director')

    film_work = models.ForeignKey('Filmwork', on_delete=models.CASCADE)
    person = models.ForeignKey('Person', on_delete=models.CASCADE)
    role = models.CharField(
        max_length=2,
        choices=PersonFilmworkRole.choices,
        default=PersonFilmworkRole.ACTOR,
    )
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "content\".\"person_film_work"
