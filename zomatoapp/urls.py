from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('search/', views.search_restaurant, name='search_restaurant'),
    path('recommend/', views.recommend_restaurants, name='recommend'),
    path('contact/', views.contact, name='contact'),
]
