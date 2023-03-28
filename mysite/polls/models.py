

import datetime
from django.utils import timezone
from django.db import models


class Movie(models.Model):
    title = models.CharField(max_length=200)
    release_date = models.DateTimeField('date published')
    image = models.CharField(max_length=400)
    score = models.FloatField()
    vote_count = models.IntegerField()
    overview = models.TextField()

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.release_date <= now

    def __str__(self):
        return self.title


class Choice(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    choice = models.IntegerField()
    votes = models.IntegerField(default=0)

    def __str__(self):
        return str(self.choice)
