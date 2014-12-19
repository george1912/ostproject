from django.contrib import admin

# Register your models here.
from django.contrib import admin

#importing sections for question and answers
from gproject.models import Question, Answer, Vote, UploadModel

#for answering text according to tutorial to save space
class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 3

#this creates or field sets
#date, question text, published/created date
#then we have for users
#tags
class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['question_text']}),
        ('Date Info', {'fields': ['pub_date']}),
        ('User', {'fields': ['user']}),
        ('Tags', {'fields': ['tags']}),
        ('Vote Info', {'fields': ['votes']}),
        ('Image Info', {'fields': ['image']}),
    ]
    inlines = [AnswerInline]
    list_display = ('question_text', 'pub_date', 'votes', 'user', 'image')
    search_fields = ['question_text']

#for adding in to the site
admin.site.register(Question, QuestionAdmin)
admin.site.register(Vote)
admin.site.register(UploadModel)