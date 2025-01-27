from . import views
from django.urls import path
from django.contrib.auth import views as auth_views


app_name = 'polls'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('question/<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('results/<int:question_id>/', views.ResultsView.as_view(), name='results'),
    path('vote/<int:question_id>/', views.vote, name='vote'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('add_category/', views.add_category, name='add_category'),
    path('logout/', auth_views.LogoutView.as_view(next_page='base'), name='logout'),
]

