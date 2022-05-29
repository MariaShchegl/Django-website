from django.urls import path, include
from . import views

app_name='backend'

urlpatterns = [
    path('login', views.signin, name='login'),
    path('signup', views.signup, name='signup'),
    path('logout', views.logOut, name='logout'),
    path('update/<int:id>', views.update, name='update'),
    path('delete/<int:id>', views.remove, name='remove'),
    path('create/recipe', views.store, name='create'),
]