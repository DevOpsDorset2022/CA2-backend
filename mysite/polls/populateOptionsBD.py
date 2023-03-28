from polls.models import Choice

for i in range(1, 9981):
    for j in range(1, 11):
        choice = Choice()
        choice.movie = i
        choice.choice = j
        choice.votes = 0
        choice.save()


