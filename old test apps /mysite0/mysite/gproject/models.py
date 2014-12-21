from django.db import models
from google.appengine.api import users
from django.contrib.auth.models import User
import datetime


class UploadModel(models.Model):
    file = models.FileField(upload_to='uploads/%Y/%m/%d/%H/%M/%S/')
    filename = models.CharField(max_length=600, default=' ')

    def __str__(self):         
        return self.filename

class Question(models.Model):
    question_text = models.TextField()
    pub_date = models.DateTimeField(default = datetime.datetime.now())
    user = models.ForeignKey(User, null=True, blank=True)
    votes = models.IntegerField(default=0)
    tags = models.CharField(max_length=500, default=' ')
    image = models.ForeignKey(UploadModel, null=True, blank=True)

    def __str__(self):           
        return self.question_text

class Answer(models.Model):
    answer_text = models.TextField()
    pub_date = models.DateTimeField(default = datetime.datetime.now())
    user = models.ForeignKey(User, null=True, blank=True)
    votes = models.IntegerField(default=0)
    image = models.ForeignKey(UploadModel, null=True, blank=True, default=0)
    question_id=models.ForeignKey(Question, null=True, blank=True)

    def __str__(self):            
        return self.answer_text

class Vote(models.Model):
    vote_text = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, null=True, blank=True)
    question_id=models.ForeignKey(Question)
    answer_id=models.ForeignKey(Answer, null=True, blank=True, default=0)
    NONE = 0
    UP = 1
    DOWN = -1
    CHOICES = ( 
        (NONE, 'None'),
        (UP, 'Up'),
        (DOWN, 'Down'),
    )
    up_or_down = models.IntegerField(choices=CHOICES, default=0)

    def __str__(self):              # __unicode__ on Python 2
        return self.vote_text
