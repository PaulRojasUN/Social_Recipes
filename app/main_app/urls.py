from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    path('create_recipe/', views.create_recipe, name='create_recipe'),
    path('edit_recipe/<int:id>/', views.edit_recipe, name='edit_recipe'),
    path('view_recipe/<int:id>/', views.view_recipe, name='view_recipe'),
    path('view_account/<slug:username>/', views.view_account, name='view_account'),
    path('edit_account/<slug:username>/', views.edit_account , name='edit_account'),
    path('social/<int:id>/', views.social, name='social'),
    path('filter/', views.filter, name='filter'),
]
