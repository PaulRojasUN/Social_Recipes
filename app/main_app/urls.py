from django.urls import path
from django.contrib.auth import views as auth_views
from . import views, post_views, view_utils

urlpatterns = [

    # RENDERING ENDPOINTS
    path('', views.home, name='home'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    path('create_recipe/', views.create_recipe, name='create_recipe'),
    path('edit_recipe/<int:id>/', views.edit_recipe, name='edit_recipe'),
    path('view_recipe/<int:id>/', views.view_recipe, name='view_recipe'),
    path('view_account/<slug:username>/', views.view_account, name='view_account'),
    path('edit_account/<slug:username>/', views.edit_account , name='edit_account'),
    path('social/<slug:username>/', views.social, name='social'),
    path('filter/', views.filter, name='filter'),
    path('search/', views.search, name='search'),

    # POST ENDPOINTS
    path('add_following/', post_views.add_following, name='add_following'),

    # UTILS

    path('prepare_view_account/<slug:target_username>', view_utils.prepare_view_account, name='prepare_view_account'),
]
