from operator import index
from django import views
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    # path('', views.index, name='index'),
    # path('settings', views.settings, name='settings'),
    # path('upload', views.upload, name='upload'),
    # path('follow', views.follow, name='follow'),
    # path('search', views.search, name='search'),
    # path('profile', views.profile, name='profile'),
    # path('e_profile', views.e_profile, name='e_profile'),
    # path('like-post', views.like_post, name='like-post'),
    path('signup', views.signup, name='signup'),
    path('signin', views.signin, name='signin'),
    path('logout', views.logout, name='logout'),
]