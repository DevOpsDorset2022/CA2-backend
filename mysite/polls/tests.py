from django.core.exceptions import ValidationError
import datetime
from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from .models import Movie, Choice


class QuestionModelTests(TestCase):

    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() returns False for questions whose release_date
        is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Movie(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """
        was_published_recently() returns False for questions whose release_date
        is older than 1 day.
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Movie(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently() returns True for questions whose release_date
        is within the last day.
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Movie(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)


def create_question(question_text, days):
    """
    Create a movie with the given `title` and published the
    given number of `days` offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Movie.objects.create(question_text=question_text, pub_date=time)


class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        """
        If no questions exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_question(self):
        """
        Questions with a release_date in the past are displayed on the
        index page.
        """
        question = create_question(question_text="Past movie.", days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question],
        )

    def test_future_question(self):
        """
        Questions with a release_date in the future aren't displayed on
        the index page.
        """
        create_question(question_text="Future movie.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_future_question_and_past_question(self):
        """
        Even if both past and future questions exist, only past questions
        are displayed.
        """
        question = create_question(question_text="Past movie.", days=-30)
        create_question(question_text="Future movie.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question],
        )

    def test_two_past_questions(self):
        """
        The questions index page may display multiple questions.
        """
        question1 = create_question(question_text="Past movie 1.", days=-30)
        question2 = create_question(question_text="Past movie 2.", days=-5)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question2, question1],
        )


class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        """
        The detail view of a movie with a release_date in the future
        returns a 404 not found.
        """
        future_question = create_question(question_text='Future movie.', days=5)
        url = reverse('polls:detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """
        The detail view of a movie with a release_date in the past
        displays the movie's text.
        """
        past_question = create_question(question_text='Past Movie.', days=-5)
        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.title)


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
