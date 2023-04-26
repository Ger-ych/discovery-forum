from . import models


# function to calculate the rating of an answer
def calc_answer_rating(answer):
    answer.rating = 0
    for r in answer.rates.all():
        answer.rating += int(r.rate)

    answer.save()
