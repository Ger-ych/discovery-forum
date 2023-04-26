from django.contrib import admin
from .models import Answer, AnswerComment, AnswerRate


# adding answer comment inline
class AnswerCommentInline(admin.StackedInline):
    model = AnswerComment
    fields = ('user', 'text', 'date_time' )
    readonly_fields = ('date_time', )

    verbose_name = 'Комментарий'
    verbose_name_plural = 'Комментарии к ответу'

# adding answer rate inline
class AnswerRateInline(admin.StackedInline):
    model = AnswerRate
    fields = ('user', 'rate' )

    verbose_name = 'Оценка'
    verbose_name_plural = 'Оценки ответа'

# registration of answer model in administration
@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    inlines = (AnswerCommentInline, AnswerRateInline )

    list_display = ("user", "question", "heading", "rating", "is_solution", "date_time")

    fieldsets = (
        (None, {'fields': ('user', 'question', 'date_time', 'is_solution')}),
        (None, {
            'fields': ('heading', 'text', 'rating'),
        }),
    )

    readonly_fields = ("date_time", "rating" )

    list_filter = ('user', 'question', 'is_solution')

    save_on_top = True
