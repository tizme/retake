from django.conf.urls import url, include
from django.contrib import admin
from . import views
urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^quotes$', views.quotes),
    url(r'^addquote$', views.addquote),
    url(r'^favorite/(?P<id>\d+)$', views.favorite),
    url(r'^unfavorite/(?P<id>\d+)$', views.unfavorite),
    url(r'^user/(?P<id>\d+)$', views.user)
]
