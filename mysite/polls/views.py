from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from .models import Choice, Movie


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_movie_list'

    def get_queryset(self):
        """
        Return the last ten published questions (not including those set to be
        published in the future).
        """
        return Movie.objects.filter(
            release_date__lte=timezone.now()
        ).order_by('-release_date')[:]


class DetailView(generic.DetailView):
    model = Movie
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Movie.objects.filter(release_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Movie
    template_name = 'polls/results.html'


def vote(request, question_id):
    question = get_object_or_404(Movie, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the movie voting form.
        return render(request, 'polls/detail.html', {
            'movie': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))


def results(request, question_id):
    question = get_object_or_404(Movie, pk=question_id)
    return render(request, 'polls/results.html', {'movie': question})


def delete(request, question_id):
    question = get_object_or_404(Movie, pk=question_id)
    question.delete()
    return HttpResponseRedirect(reverse('polls:index'))

