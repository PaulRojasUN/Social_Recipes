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
    path('edit_post/<slug:id>/', views.edit_post, name='edit_post'),
    path('view_post/<slug:id>/', views.view_post, name='view_post'),
    path('view_account/<slug:username>/', views.view_account, name='view_account'),
    path('edit_account/<slug:username>/', views.edit_account , name='edit_account'),
    path('social/<slug:username>/', views.social, name='social'),
    path('filter/', views.filter, name='filter'),
    path('search/', views.search, name='search'),
    path('tags_manager/', views.tags_manager, name='tags_manager'),
    path('admin_manage_users/', views.admin_manage_users, name='admin_manage_users'),
    path('tags_management/', views.tags_management, name='tags_management'),
    path('ingredients_management/', views.ingredients_management, name='ingredients_management'),
    
    # POST ENDPOINTS
    path('add_following/', post_views.add_following, name='add_following'),
    path('add_remove_moderator/', post_views.add_remove_moderator, name='add_remove_moderator'),
    path('create_tag/', post_views.create_tag, name='create_tag'),
    path('set_classified_tag/', post_views.set_classified_tag, name='set_classified_tag'),
    path('edit_account_fields/', post_views.edit_account_fields, name='edit_account_fields'),
    path('create_ingredient/', post_views.create_ingredient, name='create_ingredient'),
    path('set_classified_ingredient/', post_views.set_classified_ingredient, name='set_classified_ingredient'),
    path('propose_new_ingredient/', post_views.propose_new_ingredient, name='propose_new_ingredient'),
    path('propose_new_tag/', post_views.propose_new_tag, name='propose_new_tag'),
    path('create_new_post/', post_views.create_new_post, name='create_new_post'),
    path('edit_post/', post_views.edit_post, name='edit_post'),
    path('add_remove_like_post/', post_views.add_remove_like_post, name='add_remove_like_post'),
    path('increment_post_seed/', post_views.increment_post_seed, name='increment_post_seed'),
    path('reset_posts/', post_views.reset_posts, name='reset_posts'),

    # UTILS ENDPOINTS
    path('prepare_view_account/<slug:target_username>', view_utils.prepare_view_account, name='prepare_view_account'),
    path('predict_username/<slug:username>', view_utils.predict_username, name='predict_username'),
    path('get_user_username/<slug:username>', view_utils.get_user_username, name='get_user_username'),
    path('prepare_admin_manage_users/<slug:username>', view_utils.prepare_admin_manage_users, name='prepare_admin_manage_users'),
    path('get_tag_information/<slug:tag_name>', view_utils.get_tag_information, name='get_tag_information'),
    path('get_interested_tags_user/<slug:username>', view_utils.get_interested_tags_user, name='get_interested_tags_user'),
    path('get_ingredient_information/<slug:ingredient_name>', view_utils.get_ingredient_information, name='get_ingredient_information'),
    path('get_post_information/<slug:id>', view_utils.get_post_information, name='get_post_information'),
    path('get_homepage_posts/', view_utils.get_homepage_posts, name='get_homepage_posts'),

]
