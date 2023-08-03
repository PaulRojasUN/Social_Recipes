from django.http import HttpResponse, JsonResponse
from django.db.models import Q, Subquery, OuterRef, Count
from django.contrib.auth.decorators import login_required, user_passes_test

# User imports
from .models import FollowingUser, CustomUser

# Tags imports 
from .models import Tag, ClassifiedTag, TagUser, TagPost

# Access imports
from .models import priviliged_access, admin_access

# Ingredients imports
from .models import Ingredient, ClassifiedIngredient

# Post imports
from .models import Post, PostIngredients, PostLike, PostSeed


### Homepage ###

@login_required
def get_homepage_posts(request):
    if request.method == 'GET':
        try:

            block_size = 3;

            user = request.user;

            seed = PostSeed.objects.get_or_create(user_id=user)[0].seed;

            external_visible = FollowingUser.objects.filter(
                Q(follower_user_id=user.id) & Q(target_user_id=OuterRef('author_user_id'))
            ).values('target_user_id'
            ).annotate(followed=Count('target_user_id')
            ).values('followed');


            # Indicates if the current logged-in user has liked the posts in displays
            liked_posts = PostLike.objects.filter(
                Q(post_id=OuterRef('id'))&Q(user_id=user.id)
            ).values('post_id'
            ).annotate(likes_count=Count('id')
            ).values('likes_count');

            # Retrieve the amount of likes of each post
            posts_likes = PostLike.objects.filter(
                post_id=OuterRef('id')
            ).values('post_id'
            ).annotate(likes_count=Count('id')
            ).values('likes_count');



            posts = list(Post.objects.values(
                'id',
                'author_user_id__first_name',
                'author_user_id__username',
                'recipe_name',
                'body_text',
                'visibility',
                'post_date',
            ).annotate(liked=Subquery(liked_posts),
                       likes=Subquery(posts_likes),
                       visible=Subquery(external_visible)
            ).filter(Q(visibility=0) | Q(author_user_id=user) | Q(Q(visibility=1) & Q(visible=1)))
            .order_by('-post_date'))[seed*block_size:block_size*(seed+1)];

            return JsonResponse(posts, safe=False);
        except Exception as e:
            print(e);
            return HttpResponse('Bad request', status=400);    
    else:
        return HttpResponse('Unsupported method', status=405);
### //////// ###


### View Account ###

@login_required
def prepare_view_account(request, target_username):
    if request.method == 'GET':
        try:
            follower_username = request.user.username;
            
            if (follower_username==target_username):
                return HttpResponse('Cannot follow yourself', status=250);

            already_following = FollowingUser.objects.filter(Q(follower_user_id__username=follower_username)&
                                                             Q(target_user_id__username=target_username)).exists();
            
            if not already_following:
                return HttpResponse('Not following', status=251);
            else:
                return HttpResponse('Already following', status=252);

        except Exception as e:
            print(e);
            return HttpResponse('Wrong request', status=400);
    else:
        return HttpResponse('Unsupported method', status=405);


### /////////////////////////// ###

### Admin Manage Users ###

@user_passes_test(admin_access)
def predict_username(request, username):
    if request.method == 'GET':
        predicted_usernames = list(CustomUser.objects.filter(username__contains=username).values_list('username', flat=True)[:20]);

        return JsonResponse(predicted_usernames, safe=False);
    else:
        return HttpResponse('Unsupported method', status=405);

@user_passes_test(admin_access)
def get_user_username(request, username):
    if request.method == 'GET':
        
        try:

            user = CustomUser.objects.get(username=username);
            group = user.groups.first();
            
            if group is not None:
                group_name = group.name;    
            
                obj = {
                    'name':user.first_name,
                    'email':user.email,
                    'role':group_name,
                }

                return JsonResponse(obj);
            else:
                raise Exception("User not belonging to any group");

        except Exception as e:
            print(e);
            obj = {
                'name':'',
                'email':'',
                'group':'',
            }

            return JsonResponse(obj);
    else:
        return HttpResponse('Unsupported method', status=405);

@user_passes_test(admin_access)
def prepare_admin_manage_users(request, username):
    if request.method == 'GET':
        try:
            user = CustomUser.objects.get(username=username);
            group = user.groups.first();
            
            if group is not None:
                group_name = group.name;

                is_moderator = 1;

                if (group_name=='moderators'):
                    is_moderator = 0;

                obj = {
                    'is_moderator':is_moderator
                }

                return JsonResponse(obj);

            else:
                raise Exception("User not belonging to any group");
        except Exception:
            return HttpResponse('Bad Request', status=400);    
    else:
        return HttpResponse('Unsupported method', status=405);



### //////////////////////////////////////////// ####



### Tags Management ###



@login_required
def get_tag_information(request, tag_name):
    if request.method == 'GET':
        try:

            lower_tag_name = tag_name.lower();

            tag = Tag.objects.get(name=lower_tag_name);

            classified = 1;
            if ClassifiedTag.objects.filter(tag_id=tag).exists():
                classified = 0;

            obj = {
                'name':tag.name,
                'classified':classified,
            }
            
            return JsonResponse(obj, status= 200);
        except Exception as e:
            print(e);
            return HttpResponse('Bad request', status=400);
    else:
        return HttpResponse('Unsupported method', status=405);

### ///////////////////// ###


### Edit Account ###

@login_required
def get_interested_tags_user(request, username):
    if request.method == 'GET':
        try:
            user = CustomUser.objects.get(username=username);

            tags = list(TagUser.objects.filter(user_id=user.id).values_list('tag_id__name', flat=True));
    
            return JsonResponse(tags, safe=False);

        except Exception as e:
            print(e)
            return HttpResponse('Bad Response', status=400);    
    else:
        return HttpResponse('Unsupported method', status=405);

### /////////// ###


### get_ingredient_information ###

@login_required
def get_ingredient_information(request, ingredient_name):
    if request.method == 'GET':
        try:

            lower_ingredient_name = ingredient_name.lower();

            ingredient = Ingredient.objects.get(name=lower_ingredient_name);

            classified = 1;
            if ClassifiedIngredient.objects.filter(ingredient_id=ingredient).exists():
                classified = 0;

            obj = {
                'name':ingredient.name,
                'classified':classified,
            }
            
            return JsonResponse(obj, status=200);
        except Exception as e:
            print(e);
            return HttpResponse('Bad request', status=400);
    else:
        return HttpResponse('Unsupported method', status=405);

### //////////////////////// ###


### Edit Post ###
@login_required
def get_post_information(request, id):
    if request.method == 'GET':
        try:
            post = Post.objects.get(id=id);
        
            recipe_name = post.recipe_name;
        
            visibility_raw = post.visibility;
            
            visibility = "";
            
            if visibility_raw==0:
                visibility = 'public';
            elif visibility_raw == 1:
                visibility = 'followers_only';
            else:
                visibility = 'private';

        
            instructions = post.body_text;
        
            ingredients = list(PostIngredients.objects.filter(post_id=post).values_list('ingredient_id__name', flat=True));
        
            tags = list(TagPost.objects.filter(post_id=post).values_list('tag_id__name', flat=True));
        
            data = {
                'recipe_name':recipe_name,
                'visibility':visibility,
                'instructions':instructions,
                'ingredients':ingredients,
                'tags':tags,
            }


            return JsonResponse(data, safe=False);
        except Exception as e:
            print(e);
            return HttpResponse('An error has ocurred', status=400);    
    else:
        return HttpResponse('Unsupported method', status=405);


### //////// ###



### Search ###

@login_required
def filter_search(request):
    if request.method == 'GET':
        try:
                    
            obj = request.GET;

            user = request.user;

            users = [];

            recipes = []
          
            recipes = list(Post.objects.filter(recipe_name__contains=obj['par1']).values_list('recipe_name', flat=True));
            users = list(CustomUser.objects.filter(first_name__contains=obj['par1']).values_list('username', flat=True));

            external_visible = FollowingUser.objects.filter(
                Q(follower_user_id=user.id) & Q(target_user_id=OuterRef('author_user_id'))
            ).values('target_user_id'
            ).annotate(followed=Count('target_user_id')
            ).values('followed');

            liked_posts = PostLike.objects.filter(
               Q(post_id=OuterRef('id'))&Q(user_id=user.id)
            ).values('post_id'
            ).annotate(likes_count=Count('id')
            ).values('likes_count');

            posts_likes = PostLike.objects.filter(
                post_id=OuterRef('id')
            ).values('post_id'
            ).annotate(likes_count=Count('id')
            ).values('likes_count');

            posts = list(Post.objects.values(
                'id',
                'author_user_id__first_name',
                'author_user_id__username',
                'recipe_name',
                'body_text',
                'visibility',
                'post_date',
            ).annotate(liked=Subquery(liked_posts),
                       likes=Subquery(posts_likes),
                       visible=Subquery(external_visible)
            ).filter( Q(Q(visibility=0) | Q(author_user_id=user) | Q(Q(visibility=1) & Q(visible=1))) & 
                     Q(Q(recipe_name__in=recipes) | Q(author_user_id__username__in=users)))
            .order_by('-post_date'))[:10];

            return JsonResponse(posts, safe=False);
    
        except Exception as e:
            print(e);
            return HttpResponse('An error has ocurred', status=400);        
    else: 
        return HttpResponse('Unsupported method', status=405);
### ////// ###
