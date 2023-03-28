from datetime import timedelta
from django.test import TestCase
from django.utils import timezone
from polls.models import Movie, Choice


class MovieTests(TestCase):
    def setUp(self):
        # Create a Movie object for testing
        self.movie = Movie.objects.create(
            title='Test Movie',
            release_date=timezone.now() - timedelta(days=1),
            image='test_image.jpg',
            score=7.5,
            vote_count=100,
            overview='This is a test movie.'
        )

    def test_movie_was_published_recently(self):
        # Test the was_published_recently() method for a recent movie
        recent_movie = Movie.objects.create(
            title='Recent Movie',
            release_date=timezone.now() - timedelta(hours=1),
            image='recent_image.jpg',
            score=8.0,
            vote_count=200,
            overview='This is a recent movie.'
        )
        self.assertTrue(recent_movie.was_published_recently())

        # Test the was_published_recently() method for an old movie
        old_movie = Movie.objects.create(
            title='Old Movie',
            release_date=timezone.now() - timedelta(days=30),
            image='old_image.jpg',
            score=6.0,
            vote_count=50,
            overview='This is an old movie.'
        )
        self.assertFalse(old_movie.was_published_recently())

    def test_movie_str(self):
        # Test the __str__() method for a movie
        self.assertEqual(str(self.movie), 'Test Movie')

    def test_choice_str(self):
        # Test the __str__() method for a choice
        choice = Choice.objects.create(movie=self.movie, choice=1, votes=10)
        self.assertEqual(str(choice), '1')
