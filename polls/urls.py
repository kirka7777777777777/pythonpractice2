from . import views
from django.urls import path
from django.contrib.auth import views as auth_views
from django.urls import path
from .views import ApplicationListView, ApplicationCreateView

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
    path('application/create/', views.create_application, name='create_application'),
    path('logout/', auth_views.LogoutView.as_view(next_page='base'), name='logout'),
    path('', views.homepage, name='homepage'),
    path('applications/', ApplicationListView.as_view(), name='application_list'),
    path('applications/create/', ApplicationCreateView.as_view(), name='application_create'),
    path('applications/user/', views.user_applications, name='user_applications'),
    path('applications/delete/<int:application_id>/', views.delete_application, name='delete_application'),
    path('admin/applications/change_status/<int:application_id>/', views.change_application_status, name='change_application_status'),
    path('admin/categories/', views.admin_category_list, name='admin_category_list'),
    path('admin/categories/create/', views.admin_category_create, name='admin_category_create'),
    path('admin/categories/delete/<int:category_id>/', views.admin_category_delete, name='admin_category_delete'),
    path('admin/applications/', views.admin_application_list, name='admin_application_list'),
]

