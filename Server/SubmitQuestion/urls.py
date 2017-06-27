from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^postMultipleQuestion$', views.postMultipleQuestion, name='postMultipleQuestion'),
    url(r'^postBooleanQuestion$', views.postBooleanQuestion, name='postBooleanQuestion'),
    url(r'^getUserSubmitQuestion$', views.getUserSubmitQuestion, name='getUserSubmitQuestion'),
]