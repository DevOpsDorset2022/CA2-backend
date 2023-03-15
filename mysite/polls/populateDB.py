import json
from datetime import datetime

import requests
from polls.models import Movie


# class Movie2:
#     def __init__(self, title, release_date, score, image_path):
#         self.title = title
#         self.release_date = release_date
#         self.score = score
#         self.image_path = image_path
#
#     def __str__(self):
#         return "Title:" + self.title + " Score:" + str(self.score)
def is_json_key_present(json2, key):
    try:
        buf = json2[key]
    except KeyError:
        return False

    return True


def check_date_format(date_string, date_format):
    try:
        datetime.strptime(date_string, date_format)
        # print(dummy)
        return True
    except ValueError:
        return False


movies = []

for i in range(1, 500):
    req = requests.get(
        'https://api.themoviedb.org/3/discover/movie?sort_by=popularity.desc&api_key=04c35731a5ee918f014970082a0088b1'
        '&page=' + str(i))
    json_data = json.loads(req.text)
    page = json_data['page']
    print(page)
    for element in json_data['results']:
        movie = Movie()
        movie.title = element['title']

        if is_json_key_present(element, 'release_date'):
            if check_date_format(element['release_date'], '%Y-%m-%d') and isinstance(element['release_date'], str):
                movie.release_date = element['release_date'] + " 00:00:00+00:00"
            else:
                movie.release_date = "1900-01-01 00:00:00+00:00"
        else:
            movie.release_date = "1900-01-01 00:00:00+00:00"
        if is_json_key_present(element, 'poster_path'):
            movie.image = "https://image.tmdb.org/t/p/w1280" + str(element['poster_path'])
        else:
            movie.image = " "
        movie.score = element['vote_average']
        movie.save()
        movies.append(movie)

for movie in movies:
    print(movie.title)
    print(movie.release_date)
    print(movie.score)
    print(movie.image)
