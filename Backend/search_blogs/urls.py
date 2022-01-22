from django.urls import path
from .import views
from django.conf.urls import url


urlpatterns = [
    url('search/$', views.SearchView.as_view()),
    url('search/suggest', views.SearchSuggest.as_view())
]