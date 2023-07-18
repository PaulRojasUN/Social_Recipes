from django.urls import path
from django.contrib.auth import views as auth_views
from . import views, post_views, view_utils

urlpatterns = [

    # RENDERING ENDPOINTS
    path('', views.home, name='home'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    path('create_post/', views.create_post, name='create_post'),
    path('edit_post/<int:id>/', views.edit_post, name='edit_post'),
    path('view_post/<int:id>/', views.view_post, name='view_post'),
    path('view_account/<slug:username>/', views.view_account, name='view_account'),
    path('edit_account/<slug:username>/', views.edit_account , name='edit_account'),
    path('social/<slug:username>/', views.social, name='social'),
    path('filter/', views.filter, name='filter'),
    path('search/', views.search, name='search'),
    path('tags_manager/', views.tags_manager, name='tags_manager'),
    path('admin_manage_users/', views.admin_manage_users, name='admin_manage_users'),
    path('tags_management/', views.tags_management, name='tags_management'),
    
    # POST ENDPOINTS
    path('add_following/', post_views.add_following, name='add_following'),

    # UTILS
    path('prepare_view_account/<slug:target_username>', view_utils.prepare_view_account, name='prepare_view_account'),
    path('predict_username/<slug:username>', view_utils.predict_username, name='predict_username'),
    path('get_user_username/<slug:username>', view_utils.get_user_username, name='get_user_username'),
    path('prepare_admin_manage_users/<slug:username>', view_utils.prepare_admin_manage_users, name='prepare_admin_manage_users'),
    path('add_remove_moderator/', view_utils.add_remove_moderator, name='add_remove_moderator'),
    path('create_tag/', view_utils.create_tag, name='create_tag'),
]
