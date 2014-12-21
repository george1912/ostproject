from django.conf.urls import patterns, include, url

from gproject.views import QFeed

from gproject import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'gproject.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

  
	#for the root directory folder
    url(r'^$', views.index, name='index'),
    #for login
    url(r'^login/$', views.login, name='login'),
    #for searching
    url(r'^search/$', views.search, name='search'),
    #for uploading content
    url(r'^upload/$', views.upload, name='upload'),
    #for downloading content
    url(r'^download/(?P<pk>.+)$', views.download, name= 'download'),
    #for adding a question
    url(r'^add_question/$', views.add_question, name='add_question'),
    #for viewing count of view
    url(r'^add_answer/(?P<question_id>\d+)/$', views.add_answer, name='add_answer'),
    #for viewing count of view
    url(r'^edit_answer/(?P<answer_id>\d+)/$', views.edit_answer, name='edit_answer'),
    
    url(r'^(?P<question_id>\d+)/$', views.question_detail, name='question_detail'),
    
    url(r'^(?P<question_id>\d+)/edit_question$', views.edit_question, name='edit_question'),
  
    url(r'^(?P<question_id>\d+)/vote_q/$', views.vote_question, name='vote_question'),
    
    url(r'^(?P<question_id>\d+)/results/$', views.results, name='results'),
   
    url(r'^(?P<question_id>\d+)/vote_a/$', views.vote_answer, name='vote_answer'),
    #for the RSS FEED for questions!
    url(r'^(?P<question_id>\d+)/feed$', QFeed()),
)