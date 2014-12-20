from django import forms
from django.forms import ModelForm
from gproject.models import Question, Answer, Vote, UploadModel

class CreateQuestionForm(ModelForm):
    class Meta:
        model = Question
        fields = ['question_text', 'tags', 'image']

class CreateAnswerForm(ModelForm):
    class Meta:
        model = Answer
        fields = ['answer_text', 'image']

class EditQuestionForm(ModelForm):
    class Meta:
        model = Question
        fields = ['question_text', 'tags', 'image']

class EditAnswerForm(ModelForm):
    class Meta:
        model = Answer
        fields = ['answer_text', 'image']

class UploadForm(forms.ModelForm):
    class Meta:
        model = UploadModel
        fields = ['file', 'filename']