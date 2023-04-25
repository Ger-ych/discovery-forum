from django.contrib import admin
from .models import QuestionCategory, Question, QuestionComment


# registration of question category model in administration
@admin.register(QuestionCategory)
class QuestionCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", )
    fields = ("name", )

# adding an image inline to a product
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

    list_display = ("user", "heading", "category")

    fieldsets = (
        (None, {'fields': ('user', 'date_time', 'category', 'following_users')}),
        (None, {
            'fields': ('heading', 'text', 'keywords'),
        }),
    )

    readonly_fields = ("date_time", )

    list_filter = ('user', 'category')

    save_on_top = True
