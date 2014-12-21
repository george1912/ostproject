from django.conf.urls.defaults import *
from django.contrib import admin
#adding extra django views
from django.conf.urls import patterns
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView

import dbindexer

handler500 = 'djangotoolbox.errorviews.server_error'

# django admin
admin.autodiscover()

# search for dbindexes.py in all INSTALLED_APPS and load them
dbindexer.autodiscover()

#updating URL Patterns! for login and making the views
urlpatterns = patterns('',
    ('^_ah/warmup$', 'djangoappengine.views.warmup'),
    ('^_ah/login_required$', 'djangoappengine.views.warmup'),
    ('^$', 'gproject.views.index'),
    ('^admin/', include(admin.site.urls)),
    ('^gproject/', include('gproject.urls', namespace="gproject")),
)
