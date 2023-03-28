from django.core.exceptions import ValidationError
import datetime
from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from .models import Movie, Choice


class TestModels(TestCase):
    def test_was_published_recently_with_future_movie(self):
        """
        was_published_recently() returns False for movies whose release_date
        is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_movie = Movie(release_date=time)
        self.assertIs(future_movie.was_published_recently(), False)

    def test_was_published_recently_with_old_movie(self):
        """
        was_published_recently() returns False for movies whose release_date
        is older than 1 day.
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_movie = Movie(release_date=time)
        self.assertIs(old_movie.was_published_recently(), False)

    def test_was_published_recently_with_recent_movie(self):
        """
        was_published_recently() returns True for movies whose release_date
        is within the last day.
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_movie = Movie(release_date=time)
        self.assertIs(recent_movie.was_published_recently(), True)

    def test_movie_title(self):
        """
        Movie model is created with title and other required fields.
        """
        movie = Movie.objects.create(title="Test Movie", release_date=timezone.now(),
                                     image="test_image.jpg", score=8.5, vote_count=1234, overview="test overview")
        self.assertEqual(str(movie), movie.title)

    def test_movie_release_date(self):
        """
        Movie model fields release_date should be saved correctly
        """
        release_date = timezone.now()
        movie = Movie(release_date=release_date)
        self.assertEqual(movie.release_date, release_date)

    def test_movie_image(self):
        """
        Movie model fields image should be saved correctly
        """
        movie = Movie(image="http://example.com/image.png")
        self.assertEqual(movie.image, "http://example.com/image.png")

    def test_movie_score(self):
        """
        Movie model fields score should be saved correctly
        """
        movie = Movie(score=7.5)
        self.assertEqual(movie.score, 7.5)

    def test_movie_vote_count(self):
        """
        Movie model fields vote_count should be saved correctly
        """
        movie = Movie(vote_count=1000)
        self.assertEqual(movie.vote_count, 1000)

    def test_movie_overview(self):
        """
        Movie model fields overview should be saved correctly
        """
        movie = Movie(overview="Movie overview")
        self.assertEqual(movie.overview, "Movie overview")

    def test_movie_str(self):
        """
        Movie model __str__ method should return movie title
        """
        movie = Movie(title="Movie Title")
        self.assertEqual(str(movie), "Movie Title")

    def test_choice_movie(self):
        """
        Choice model fields movie should be saved correctly
        """
        movie = Movie(title="Movie Title")
        choice = Choice(movie=movie)
        self.assertEqual(choice.movie, movie)

    def test_choice_choice(self):
        """
        Choice model fields choice should be saved correctly
        """
        choice = Choice(choice=1)
        self.assertEqual(choice.choice, 1)

    def test_choice_votes(self):
        """
        Choice model fields votes should be saved correctly
        """
        choice = Choice(votes=5)
        self.assertEqual(choice.votes, 5)

    def test_choice_str(self):
        """
        Choice model __str__ method should return choice as string
        """
        choice = Choice(choice=1)
        self.assertEqual(str(choice), "1")

    def test_choice_movie_relation(self):
        """
        Choice model is created with movie foreign key relation.
        """
        movie = Movie.objects.create(title="Test Movie", release_date=timezone.now(),
                                     image="test_image.jpg", score=8.5, vote_count=1234, overview="test overview")
        choice = Choice.objects.create(movie=movie, choice=1)
        self.assertEqual(choice.movie, movie)

    def test_choice_movie_relation_with_deleted_movie(self):
        """
        Choice model does not exist if the related movie is deleted.
        """
        movie = Movie.objects.create(title="Test Movie", release_date=timezone.now(),
                                     image="test_image.jpg", score=8.5, vote_count=1234, overview="test overview")
        choice = Choice.objects.create(movie=movie, choice=1)
        movie.delete()
        choice_exists = Choice.objects.filter(id=choice.id).exists()
        self.assertFalse(choice_exists)

    def test_movie_score_range(self):
        """
        The score field can store a float value between 0 and 10.
        """
        movie = Movie(title="Pulp Fiction", score=8.9)
        self.assertEqual(movie.score, 8.9)
        with self.assertRaises(ValidationError):
            movie.score = -1
            movie.full_clean()
        with self.assertRaises(ValidationError):
            movie.score = 11
            movie.full_clean()


class IndexViewTests(TestCase):
    def test_no_movies(self):
        """
        If no movies exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No movies are available.")
        self.assertQuerysetEqual(response.context['latest_movie_list'], [])

    def test_past_movie(self):
        """
        Movies with a release date in the past are displayed on the index page.
        """
        Movie.objects.create(title="Past movie", release_date=timezone.now() - datetime.timedelta(days=1),
                     image="some path", score=0, vote_count=0, overview="some overview")
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_movie_list'],
            ['<Movie: Past movie>']
        )

    def test_future_movie(self):
        """
        Movies with a release date in the future aren't displayed on the index page.
        """
        Movie.objects.create(title="Future movie", release_date=timezone.now() + datetime.timedelta(days=30),
                     image="some path", score=0, vote_count=0, overview="some overview")
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No movies are available.")
        self.assertQuerysetEqual(response.context['latest_movie_list'], [])


class ResultsViewTest(TestCase):
    def test_no_results(self):
        """
        If no movies exist, an appropriate message should be displayed.
        """
        response = self.client.get(reverse('polls:results', args=(1,)))
        self.assertEqual(response.status_code, 404)

    def test_movie_with_choices(self):
        """
        If a movie exists and has choices, the choices should be displayed.
        """
        movie = Movie.objects.create(title='Test Movie', release_date=timezone.now(), image="some path", score=0, vote_count=0, overview="some overview")
        choice1 = Choice.objects.create(movie=movie, choice=1, votes=0)
        choice2 = Choice.objects.create(movie=movie, choice=2, votes=0)
        response = self.client.get(reverse('polls:results', args=(movie.id,)))
        self.assertContains(response, choice1.choice)
        self.assertContains(response, choice2.choice)


class VoteViewTest(TestCase):
    def test_voting_for_nonexistent_movie(self):
        """
        If the user tries to vote for a nonexistent movie, they should see a 404 error.
        """
        response = self.client.post(reverse('polls:vote', args=(1,)), {'choice': 1})
        self.assertEqual(response.status_code, 404)

    def test_voting_for_movie_with_choices(self):
        """
        If the user votes for a movie with choices, the vote count and score should be updated.
        """
        movie = Movie.objects.create(title='Test Movie', release_date=timezone.now(), image="some path", score=0, vote_count=0, overview="some overview")
        choice1 = Choice.objects.create(movie=movie, choice=1, votes=0)
        choice2 = Choice.objects.create(movie=movie, choice=2, votes=0)
        response = self.client.post(reverse('polls:vote', args=(movie.id,)), {'choice': choice1.id})
        movie.refresh_from_db()
        self.assertEqual(movie.vote_count, 1)
        self.assertEqual(movie.score, int(choice1.choice) / 2)
        choice1.refresh_from_db()
        self.assertEqual(choice1.votes, 1)

    def test_voting_with_no_choice_selected(self):
        """
        If the user tries to vote without selecting a choice, they should see an error message.
        """
        movie = Movie.objects.create(title='Test Movie', release_date=timezone.now(), image="some path", score=0, vote_count=0, overview="some overview")
        choice1 = Choice.objects.create(movie=movie, choice=1, votes=0)
        response = self.client.post(reverse('polls:vote', args=(movie.id,)), {})
        self.assertContains(response, "You didn't select a choice.")

    def test_delete(self):
        """
        Test that deleting a movie works and redirects to the index page.
        """
        movie = Movie.objects.create(title='Test Movie', release_date=timezone.now(), image="some path", score=0, vote_count=0, overview="some overview")
        url = reverse('polls:delete', args=(movie.id,))
        response = self.client.post(url)
        self.assertRedirects(response, reverse('polls:index'))


