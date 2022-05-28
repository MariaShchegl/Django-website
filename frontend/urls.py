from django.urls import path, include
from . import views

urlpatterns = [
    path('recipe/<int:id>/edit', views.edit),
    path('recipe/<int:id>/', views.show),
    path('account/', views.account, name='account'),
    path('', views.index, name='index'),
]