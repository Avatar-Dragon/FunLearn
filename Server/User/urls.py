from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login$', views.login, name='login'),
    url(r'^register$', views.register, name='register'),
    url(r'^getScore$', views.getScore, name='getScore'),
    url(r'^updateScore$', views.updateScore, name='updateScore'),
    url(r'^userInformation$', views.getUserInformation, name='userInformation'),
]