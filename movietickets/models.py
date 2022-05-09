from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q

lang_choice=(
	('SPANISH','Spanish'),
    ('ENGLISH','English'),
    ('FRENCH','French'),
    ('GERMANY','Germany'),
    ('POLISH','Polish'),
    ('CHINESE','Chinese'),
)

class MovieQuerySet(models.query.QuerySet):
    def search(self,query):
        lookup = (
            Q(name__icontains=query)|
            Q(director__icontains=query)|
            Q(description__icontains=query)|
            Q(trailer__icontains=query)|
            Q(cast__icontains=query)
        )
        return self.filter(lookup).distinct()

class MovieManager(models.Manager):
    def get_queryset(self):
        return MovieQuerySet(self.model,self._db)
    def search(self,query):
        return self.get_queryset().search(query)

class Movie(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    cast = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    rating = models.DecimalField(max_digits=2, decimal_places=1)
    director = models.CharField(max_length=50)
    year = models.IntegerField(verbose_name='Produced Year')
    length = models.IntegerField(verbose_name='Length', help_text='Enter run length in minutes')
    language = models.CharField(max_length=10,choices=lang_choice)
    trailer = models.CharField(max_length=100)  
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = MovieManager()

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name

class Ticket(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user',
        blank=True,
        null=True
    )
    movie = models.ForeignKey(
        Movie,
        on_delete=models.CASCADE,
        related_name='movie',
    )
    created_at = models.DateTimeField(auto_now_add=True)

