from django.contrib import admin
from .models import QuestionCategory, Question, QuestionComment


# registration of question category model in administration
@admin.register(QuestionCategory)
class QuestionCategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", )
    fields = ("id", "name", )
    readonly_fields = ('id', )

# adding question comment inline
class QuestionCommentInline(admin.StackedInline):
    model = QuestionComment
    fields = ('user', 'text', 'date_time' )
    readonly_fields = ('date_time', )

    verbose_name = 'Комментарий'
    verbose_name_plural = 'Комментарии к вопросу'

# registration of question model in administration
@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    inlines = (QuestionCommentInline, )

    list_display = ("id", "user", "heading", "category", "date_time")

    fieldsets = (
        (None, {'fields': ('id', 'user', 'date_time', 'category', 'following_users')}),
        (None, {
            'fields': ('heading', 'text', 'keywords'),
        }),
    )

    readonly_fields = ('id', "date_time", )

    list_filter = ('user', 'category', 'date_time')

    save_on_top = True
