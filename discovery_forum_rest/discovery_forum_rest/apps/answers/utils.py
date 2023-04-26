from . import models


# function to calculate the rating of an answer
def calc_answer_rating(answer):
    answer_rates = models.AnswerRate.objects.filter(answer=answer)

    answer.rating = 0
    for r in answer_rates:
        answer.rating += int(r.rate)

    answer.save()
