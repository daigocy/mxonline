# encoding:utf-8
from django.conf.urls import url

from .views import add_ask, add_fav, add_comment

urlpatterns = [
    url(r'^add_ask', add_ask, name='add_ask'),
    url(r'^add_fav', add_fav, name='add_fav'),
    url(r'^add_comment', add_comment, name='add_comment'),
]
