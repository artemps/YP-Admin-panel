from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from .abstract import TimeStampedMixin, UUIDMixin


class Filmwork(UUIDMixin, TimeStampedMixin):

    class FilmworkType(models.TextChoices):
        MOVIE = _('movie')
        TV_SHOW = _('tv_show')

    title = models.CharField(verbose_name=_('Title'), max_length=255)
    description = models.TextField(verbose_name=_('Description'), blank=True)
    creation_date = models.DateField(verbose_name=_('Release date'), blank=True, null=True)
    rating = models.FloatField(
        verbose_name=_('Rating'),
        blank=True,
        null=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    type = models.CharField(
        max_length=7,
        choices=FilmworkType.choices,
        default=FilmworkType.MOVIE,
    )
    genres = models.ManyToManyField('Genre', through='GenreFilmwork')
    persons = models.ManyToManyField('Person', through='PersonFilmwork')

    class Meta:
        db_table = "content\".\"film_work"
        verbose_name = _('Filmwork')
        verbose_name_plural = _('Filmworks')
        indexes = [
            models.Index(fields=["title"], name='film_work_title_idx'),
            models.Index(fields=["creation_date", "rating"])
        ]

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
        indexes = [
            models.Index(fields=["full_name"], name='person_full_name_idx')
        ]

    def __str__(self):
        return self.full_name


class GenreFilmwork(UUIDMixin):
    film_work = models.ForeignKey('Filmwork', on_delete=models.CASCADE)
    genre = models.ForeignKey('Genre', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "content\".\"genre_film_work"
        constraints = [
            models.UniqueConstraint(fields=['film_work', 'genre'], name='film_work_genre_unique_idx')
        ]


class PersonFilmwork(UUIDMixin):

    class PersonFilmworkRole(models.TextChoices):
        ACTOR = _('Actor')
        WRITER = _('Writer')
        DIRECTOR = _('Director')

    film_work = models.ForeignKey('Filmwork', on_delete=models.CASCADE)
    person = models.ForeignKey('Person', on_delete=models.CASCADE)
    role = models.CharField(
        max_length=8,
        choices=PersonFilmworkRole.choices,
        default=PersonFilmworkRole.ACTOR,
    )
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "content\".\"person_film_work"
        constraints = [
            models.UniqueConstraint(fields=['film_work', 'person', 'role'], name='film_work_person_role_unique')
        ]
