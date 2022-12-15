import json
from django.utils import timezone
import requests
from polls.models import Movie


class Movie2:
    def __init__(self, title, release_date, score, image_path):
        self.title = title
        self.release_date = release_date
        self.score = score
        self.image_path = image_path

    def __str__(self):
        return "Title:" + self.title + " Score:" + str(self.score)


movies = []

for i in range(1, 2):
    req = requests.get(
        'https://api.themoviedb.org/3/discover/movie?sort_by=popularity.desc&api_key=04c35731a5ee918f014970082a0088b1'
        '&page=' + str(i))
    json_data = json.loads(req.text)
    page = json_data['page']
    print(page)
    for element in json_data['results']:
        movie = Movie2(element['title'],
                       element['release_date'] + " 00:00:00+00:00",
                       "https://image.tmdb.org/t/p/w1280" + element['poster_path'],
                       element['vote_average'])
        movies.append(movie)

for movie in movies:
    print(movie.title)
    print(movie.release_date)
    print(movie.score)
    print(movie.image_path)
