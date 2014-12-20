from django.shortcuts import get_object_or_404, render
from django.core.urlresolvers import reverse
from django.views import generic
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from filetransfers.api import prepare_upload, serve_file
from django.views.generic import TemplateView
from django.contrib.syndication.views import Feed

from google.appengine.api import users
from google.appengine.ext import webapp

import webapp2
import datetime
import re

from gproject.models import Question, Answer, Vote, UploadModel
from gproject.forms import CreateQuestionForm, CreateAnswerForm, EditQuestionForm, EditAnswerForm, UploadForm

#I can use google as my app provider
providers = {
    'Google'   : 'https://www.google.com/accounts/o8/id',
}

#creating a list of questions
#it will show 10 questions per page
def index(request):
    user = users.get_current_user()
    if user:  
        logged_in = True
        test_user(user)
    else:  
        user = ""
        logged_in = False
 
    highest_voted_q_list = Question.objects.order_by('-pub_date')
    paginator = Paginator(highest_voted_q_list, 10) 
    page = request.GET.get('page')
    try:
        questions = paginator.page(page)
    except PageNotAnInteger:
        questions = paginator.page(1)
    except EmptyPage:
        questions = paginator.page(paginator.num_pages)

    context = { 'highest_voted_q_list': questions, 'user': user, 'logged_in': logged_in }
    return render(request, 'gproject/index.html', context)

#here we define what we use to search
#what we will be going through is the number of tags
def search(request):
    user = users.get_current_user()
    search_term = request.POST['search']
    if user:  
        logged_in = True
        test_user(user)
    else:  
        user = ""
        logged_in = False
  
    highest_voted_q_list = Question.objects.order_by('-pub_date')[:10]
    search_results = []
    regex = re.compile(r'^(.+\s+)*%s(\s+.+)*$'%search_term)
    for q in highest_voted_q_list:
        tag_list = q.tags
        if regex.match(q.tags):
            search_results.append(q.id)
    highest_voted_q_list = Question.objects.filter(pk__in=search_results)
    context = { 'highest_voted_q_list': highest_voted_q_list, 'user': user, 'logged_in': logged_in, 'search_results':search_results}
    return render(request, 'gproject/index.html', context)

#we are using this to now login
#what makes this unqiue is that we have to look for any http calls
#check is user is already signed in or not
def login(request):
    user = users.get_current_user()
    response = HttpResponse()
    for name, uri in providers.items():
        provider = name
    if user:  
        response.write('Welcome Friend <em>%s</em>! [<a href="%s">sign out</a>]' % (
                user.nickname(), users.create_logout_url(request.get_full_path())))
        test_user(user)
    else:     
        response.write('Sign in: ')

        for name, uri in providers.items():
            response.write('[<a href="%s">%s</a>]' % (
                users.create_login_url(federated_identity=uri), name))
    response.write('<br><a href="/">home</a>')
    return response

#we also created a look to check is we have any users already logged in
#this is important because we need to give them the option to log in or log out

def test_user(user):
    user = users.get_current_user()
    if user:  
        try:
            db_user = User.objects.get(username=user.nickname())
        except ObjectDoesNotExist:
            u = User.objects.create_user(user.nickname())
            u.save()
    return db_user

#this is the massive infor dump for our question
def question_detail(request, question_id):
    user = users.get_current_user()
   
    if user:  
        logged_in = True
        test_user(user)
    else:  
        user = ""
        logged_in = False
   #lets get our list of votes!
    question = get_object_or_404(Question, pk=question_id)
    sum = sum_votes(question, 0)
    question.votes=sum
    question.save()
    highest_voted_a_list = question.answer_set.order_by('-votes')
    context = { 'highest_voted_a_list': highest_voted_a_list, 'question': question, 'user': user, 'logged_in': logged_in }
    return render(request, 'gproject/question_detail.html', context)

#what happens when we finish voting?
def results(request, question_id):
    user = users.get_current_user()
    if user:  
        logged_in = True
        test_user(user)
    else:  
        user = ""
        logged_in = False
        #we get back our list of results
        #we return our highest voted list
    question = get_object_or_404(Question, pk=question_id)
    highest_voted_a_list = question.answer_set.order_by('-votes')
    context = { 'highest_voted_a_list': highest_voted_a_list, 'question': question, 'user': user, 'logged_in': logged_in }
    return render(request, 'gproject/results.html', context)


#we need to see what teh user selected
#there is only two choice up or down
def vote_question(request, question_id):
    q = get_object_or_404(Question, pk=question_id)
    user = users.get_current_user()
    if user:  
        logged_in = True
        db_user = test_user(user) 
        
        if 'UP' in request.POST:
            vote = 1
        else:
            vote = -1
        try:
            v = Vote.objects.get(question_id=q, user=db_user, answer_id=0)
        except ObjectDoesNotExist:
            v = Vote(question_id=q, user=db_user, pub_date=datetime.datetime.now(), vote_text=user.nickname()+", "+q.question_text)
            v.save()
       #checking if user has voted up, summing results
        v.up_or_down = vote
        v.save()
        sum = sum_votes(q, 0)
        q.votes=sum
        q.save()
    else:  
        user = ""
        logged_in = False

    return HttpResponseRedirect(reverse('gproject:results', args=(q.id,)))


def vote_answer(request, question_id):
    q = get_object_or_404(Question, pk=question_id)
    
    user = users.get_current_user()
    if user:  
        logged_in = True
        db_user=test_user(user) 
        
        if 'UP' in request.POST:
            vote = 1
        else:
            vote = -1 
        try:
            selected_answer = q.answer_set.get(pk=request.POST['answer'])
            try:
                v = Vote.objects.get(question_id=q, answer_id=selected_answer, user=db_user)
            except ObjectDoesNotExist:
                v = Vote(question_id=q, answer_id=selected_answer, user=db_user, pub_date=datetime.datetime.now(), vote_text=user.nickname()+", "+q.question_text+", "+selected_answer.answer_text)
                v.save()
            
            v.up_or_down = vote
            v.save() 
           
            sum = sum_votes(q, selected_answer)
            selected_answer.votes=sum
            selected_answer.save()
        except (KeyError, Answer.DoesNotExist):
            # Redisplay the question voting form.
            return render(request, 'gproject/question_detail.html', {
                'question': q,
                'error_message': "You didn't select an answer.",
            })
    else:
        user = ""
        logged_in = False
    return HttpResponseRedirect(reverse('gproject:results', args=(q.id,)))

#we need to calculate the votes again

def sum_votes(question_id, answer_id):
    sum = 0
    positive_arr = Vote.objects.filter(question_id=question_id, answer_id=answer_id, up_or_down=1)
    negative_arr = Vote.objects.filter(question_id=question_id, answer_id=answer_id, up_or_down=-1)
    sum = len(positive_arr) - len(negative_arr)
    return sum

#get and post methods all over again!
#get question text from the form
def add_question(request):
    user = users.get_current_user()
    if user:  
        logged_in = True
        db_user = test_user(user)

        #adding in the published date paramters
        #if there is no form then what could happen is that a user can 
        #input text into a form
      
        if request.method == 'POST':
            form = CreateQuestionForm(request.POST)
            if form.is_valid():
                question = form.save(commit=False)
                question.user = db_user
                question.pub_date = datetime.datetime.now()  
                question.pub_date = datetime.datetime.now()
                new_text = make_links_and_photos(question.question_text)
                question.question_text = new_text             
                question.save()
                highest_voted_a_list = question.answer_set.order_by('-votes')
                context = { 'highest_voted_a_list': highest_voted_a_list, 'question': question, 'user': user, 'logged_in': logged_in }
                return render(request, 'gproject/question_detail.html', context)
        
        else:
            form = CreateQuestionForm()
    else:  
        user = ""
        logged_in = False
    return render(request, 'gproject/add_question.html', {'form': form, 'user':user , 'logged_in': logged_in})


#same as question but er are creating a form for checking and saving the answer
# if no answer there will be a blank form

def add_answer(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    user = users.get_current_user()
    if user:  
        logged_in = True
        db_user = test_user(user)
        
        if request.method == 'POST':
           
            form = CreateAnswerForm(request.POST)
            if form.is_valid():
                answer = form.save(commit=False)
                answer.user = db_user
                answer.question_id = question
                answer.pub_date = datetime.datetime.now()
                new_text = make_links_and_photos(answer.answer_text)
                answer.answer_text = new_text
                answer.save()
                question = answer.question_id
                highest_voted_a_list = question.answer_set.order_by('-votes')
                context = { 'highest_voted_a_list': highest_voted_a_list, 'question': question, 'user': user, 'logged_in': logged_in }
                return render(request, 'gproject/question_detail.html', context)
       
        else:
            form = CreateAnswerForm()
    else:  
        user = ""
        logged_in = False
    return render(request, 'gproject/add_answer.html', {'form': form, 'user':user , 'logged_in': logged_in, 'question': question})


#we needed a way in order to create texts and tags
#for this I created a unction that checks if there is an image tag via extension
#then create a link
def make_links_and_photos(question_text):
    text = question_text
    regex_html = re.compile(r'.*<a href=".*\.(jpg|png|gif)">.*')
    if regex_html.match(text):
        text = re.sub(r'<a href=', r'<img src=', text)
        text = re.sub(r'>.*</a>', r'>', text)
    return text

#for editing content (question)
#check what type of content
#check is there is the author accesing the form
#if they are they can update
#if they do update the published times

def edit_question(request, question_id): 
    instance = get_object_or_404(Question, pk=question_id)
    author = instance.user
    user = users.get_current_user()
    is_author = False
    logged_in = False
    form = EditQuestionForm()
    if user:  
        logged_in = True
        db_user=test_user(user)
        if author == db_user:
            is_author = True
        form = EditQuestionForm(request.POST or None, instance=instance)
        if form.is_valid():
            if is_author:
                question = form.save(commit=False)
                question.pub_date = datetime.datetime.now()
                new_text = make_links_and_photos(question.question_text)
                question.question_text = new_text   
                question.save()
                highest_voted_a_list = question.answer_set.order_by('-votes')
                context = { 'highest_voted_a_list': highest_voted_a_list, 'question': question, 'user': user, 'logged_in': logged_in }
                return render(request, 'gproject/question_detail.html', context)
    context = {'question': instance, 'user': user, 'logged_in': logged_in, 'form': form, 'is_author': is_author, 'author': datetime.datetime.now(), 'db_user' : db_user}
    return render(request, 'gproject/edit_question.html', context)

#for editing content (answer)
#check what type of content
#check is there is the author accesing the form
#if they are they can update
#if they do update the published times
def edit_answer(request, answer_id): 
    instance = get_object_or_404(Answer, pk=answer_id)
    author = instance.user
    user = users.get_current_user()
    is_author = False
    logged_in = False
    form = EditAnswerForm()
    if user:  
        logged_in = True
        db_user=test_user(user)
        if author == db_user:
            is_author = True
        form = EditAnswerForm(request.POST or None, instance=instance)
        if form.is_valid():
            if is_author:
                answer = form.save(commit=False)
                answer.pub_date = datetime.datetime.now()
                new_text = make_links_and_photos(answer.answer_text)
                answer.answer_text = new_text
                answer.save()
                question = answer.question_id
                highest_voted_a_list = question.answer_set.order_by('-votes')
                context = { 'highest_voted_a_list': highest_voted_a_list, 'question': question, 'user': user, 'logged_in': logged_in }
                return render(request, 'gproject/question_detail.html', context)
    context = {'answer': instance, 'user': user, 'logged_in': logged_in, 'form': form, 'is_author': is_author, 'author': datetime.datetime.now(), 'db_user' : db_user}
    return render(request, 'gproject/edit_answer.html', context)

#function for uploading data via file transwer
#call in post method with upload request
#then pull content and post via request
def upload(request):
    view_url = reverse('gproject:upload')
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        form.save()
        return HttpResponseRedirect(view_url)

    upload_url, upload_data = prepare_upload(request, view_url)
    form = UploadForm()
    return render(request, 'gproject/upload.html',
        {'form': form, 'upload_url': upload_url, 'upload_data': upload_data,
         'uploads': UploadModel.objects.all()})

#for downloading uploading content
def download(request, pk):
    upload = get_object_or_404(UploadModel, pk=pk)
    return serve_file(request, upload.file, save_as=False)

#this si for the RSS Feed for a question
class QFeed(Feed):
    title = "RSS Feed for Question!"
    link = "/feed/"
    description = "Keep up to date with this rss!"

    def get_object(self, request, question_id):
        return get_object_or_404(Question, pk=question_id)

    def description(self, obj):
        return obj.answer_set.order_by('-votes')

    def items(self, obj):
        return Question.objects.filter(pk=obj.id)

    def title(self, obj):
        return obj.question_text

    # item_link is only needed if NewsItem has no get_absolute_url method.
    def item_link(self, question):
        return reverse('gproject:question_detail', args=[question.pk])
