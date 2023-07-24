from django.http import HttpResponse
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth.models import Group
from django.db.models import Q

# User 
from .models import FollowingUser, CustomUser

# Tags
from .models import Tag, ClassifiedTag, UnclassifiedTag, TagUser, TagPost

# Access
from .models import priviliged_access, admin_access 

# Ingredients

from .models import Ingredient, ClassifiedIngredient, UnclassifiedIngredient

# Posts
from .models import Post, PostIngredients, PostLike, PostSeed


### Social ###
def add_following(request):
    if request.method == 'POST':
        print(request.POST['follower_user']);

        try:
            follower_username = request.POST['follower_user'];   
            target_username = request.POST['target_user'];   
            
            if (follower_username == target_username):
                return HttpResponse('Sorry, that is not allowed', status=400);

            already_following = FollowingUser.objects.filter(Q(follower_user_id__username=follower_username)&
                                                             Q(target_user_id__username=target_username)).exists();

            if not (already_following):
                follower_user = CustomUser.objects.get(username=follower_username);

                target_user = CustomUser.objects.get(username=target_username);

                FollowingUser.objects.create(follower_user_id=follower_user, target_user_id=target_user);

                return HttpResponse('Added Following', status=252);
            else:
                obj = FollowingUser.objects.get(Q(follower_user_id__username=follower_username)&
                                                Q(target_user_id__username=target_username));
                
                obj.delete();

                return HttpResponse('Deleted Following', status=251);
        except Exception as e:
            print(e);
            return HttpResponse('An error has ocurred', status=404);    
    else:
        return HttpResponse('Unsupported method', status=405);

### ////////////////////////////// ###



### Admin Manage Users ###

@user_passes_test(admin_access)
def add_remove_moderator(request):
    if request.method == 'POST':
        try:
            obj = request.POST;

            print(obj)

            username = obj['username'];

            user = CustomUser.objects.get(username=username);
        
            group = user.groups.first();

            if group is not None:

                group_name = group.name;
                
                user.groups.remove(group);
        
                new_group_name = "";

                if group_name=='regular_users':
                    new_group_name = 'moderators'
                else:
                    new_group_name = 'regular_users'
                
                new_group = Group.objects.get(name=new_group_name);
        
                user.groups.add(new_group);
        
                if new_group_name == 'moderators':
                    return HttpResponse('The user has been added to moderators group', status=250);
                else:
                    return HttpResponse('The user has been added to regulars users group', status=251);
            else:
                raise Exception("User not belonging to any group");
        except Exception:
            return HttpResponse('Bad Request', status=400);    
    else:
        return HttpResponse('Unsupported method', status=405);

### ////////////////// ###


### Tags Management ###

@user_passes_test(priviliged_access)
def create_tag(request):
    if request.method == 'POST':
        try:
            obj = request.POST;

            tag_name = obj['tag_name'].lower();
        
            if not tag_name:
                return HttpResponse('Not proper name given', status=460);

            already_exists = Tag.objects.filter(name=tag_name).exists();
        
            if already_exists:
                return HttpResponse('Another tag already has a similar name', status=461);
            else:
                tag = Tag.objects.create(name=tag_name);
                ClassifiedTag.objects.create(tag_id=tag);
                return HttpResponse('Tag was successfully created', status=200);
    
        except Exception:
            return HttpResponse('Bad request', status=400);
    else:
        return HttpResponse('Unsupported method', status=405);


@user_passes_test(priviliged_access)
def set_classified_tag(request):
    if request.method == 'POST':
        try:
            obj = request.POST;

            tag_name = obj['tag_name'];

            tag = Tag.objects.get(name=tag_name);

            is_unclassified = UnclassifiedTag.objects.filter(tag_id=tag).exists() and not ClassifiedTag.objects.filter(tag_id=tag).exists();

            if  is_unclassified:
                UnclassifiedTag.objects.get(tag_id=tag).delete();
                ClassifiedTag.objects.create(tag_id=tag);

                return HttpResponse('Tag set as classified', status=200);
            else:
                raise Exception('Sorry, that is not allowed');

        except Exception:
            return HttpResponse('Bad Request', status=400);
    else:
        return HttpResponse('Unsupported method', status=405);

### /////////////// ###


### Edit Account ###

@login_required
def edit_account_fields(request):
    if request.method == 'POST':
        try:
            obj = request.POST;
        
            target_username = obj['username'];

            requester_user = request.user;
        
            own_account = target_username == requester_user.username;
        
            is_admin = False;

            user_to_update = requester_user;


            if not own_account:
                if requester_user.groups.first().name == 'admin':
                    is_admin = True;
                    if CustomUser.objects.filter(username=target_username).exists():
                       user_to_update = CustomUser.objects.get(username=target_username);
                    else:
                        raise Exception('User not found');
        
            if (own_account or is_admin):
                new_name = obj['name'];


                # Update name

                if new_name == '':
                    raise Exception('Bad Name');
        
                user_to_update.first_name = new_name;
            
                # Update tags

                tags_string = obj['tags'];

                tags_list_raw = tags_string.split(',');

                tags_list = [];

                for t in tags_list_raw:
                    tags_list.append(t.lower());

                current_tags = list(TagUser.objects.filter(user_id=user_to_update).values_list('tag_id__name', flat=True));

                deleted_tags = [];

                # Save in delete_tags the tags that have been deleted
                for t in current_tags:
                    if t not in tags_list:
                        deleted_tags.append(t);

                # Assign the new tags to the user's interest tags
                for t in tags_list:
                    if not TagUser.objects.filter(Q(tag_id__name=t)&Q(user_id=user_to_update)).exists():
                        if Tag.objects.filter(name=t).filter():
                            tag = Tag.objects.get(name=t);
                            TagUser.objects.create(tag_id=tag, user_id=user_to_update);
                
                # Delete tags
                for t in deleted_tags:
                    tag = TagUser.objects.get(Q(tag_id__name=t)&Q(user_id=user_to_update));
                    tag.delete();
                
                user_to_update.save();
            
                return HttpResponse('User data has been successfully updated', status=200); 

            else:
                return HttpResponse('Forbidden', status=403);    

        except Exception as e:
            print(e);
            return HttpResponse('Bad Request', status=400);    
    else:
        return HttpResponse('Unsupported method', status=405);

### /////////// ###



### Ingredients Management ###
@user_passes_test(priviliged_access)
def create_ingredient(request):
    if request.method == 'POST':
        try:
            obj = request.POST;

            ingredient_name = obj['ingredient_name'].lower();
        
            if not ingredient_name:
                return HttpResponse('Not proper name given', status=460);

            already_exists = Ingredient.objects.filter(name=ingredient_name).exists();
        
            if already_exists:
                return HttpResponse('Another ingredient already has a similar name', status=461);
            else:
                ingredient = Ingredient.objects.create(name=ingredient_name);
                ClassifiedIngredient.objects.create(ingredient_id=ingredient);
                return HttpResponse('Ingredient was successfully created', status=200);
    
        except Exception:
            return HttpResponse('Bad request', status=400);
    else:
        return HttpResponse('Unsupported method', status=405);

@user_passes_test(priviliged_access)
def set_classified_ingredient(request):
    if request.method == 'POST':
        try:
            obj = request.POST;

            ingredient_name = obj['ingredient_name'];

            ingredient = Ingredient.objects.get(name=ingredient_name);

            in_unclassified_ingredients = UnclassifiedIngredient.objects.filter(ingredient_id=ingredient).exists();
            
            in_classified_ingredients = ClassifiedIngredient.objects.filter(ingredient_id=ingredient).exists();

            if  in_unclassified_ingredients and not in_classified_ingredients:
                UnclassifiedIngredient.objects.get(ingredient_id=ingredient).delete();
                ClassifiedIngredient.objects.create(ingredient_id=ingredient);

                return HttpResponse('Ingredient set as classified', status=200);
            else:
                raise Exception('Sorry, that is not allowed');

        except Exception:
            return HttpResponse('Bad Request', status=400);
    else:
        return HttpResponse('Unsupported method', status=405);


### ///////////////////// ###


### Create Post ###

@login_required
def propose_new_ingredient(request):
    if request.method == 'POST':
        try:
            obj = request.POST;
        
            ingredient_name = obj['ingredient_name'].lower();
        
            already_exists = Ingredient.objects.filter(name=ingredient_name).exists();
        
            if already_exists:
                return HttpResponse('Ingredient already exists', status=461);

            ingredient = Ingredient.objects.create(name=ingredient_name);

            UnclassifiedIngredient.objects.create(ingredient_id=ingredient);

            return HttpResponse('Ingredient created successfully', status=200);
        except Exception:
            return HttpResponse('Bad Request', status=400);
    else:
        return HttpResponse('Unsupported method', status=405);

@login_required
def propose_new_tag(request):
    if request.method == 'POST':
        try:
            obj = request.POST;
        
            tag_name = obj['tag_name'].lower();
        
            already_exists = Tag.objects.filter(name=tag_name).exists();
        
            if already_exists:
                return HttpResponse('tag already exists', status=461);

            tag = Tag.objects.create(name=tag_name);

            UnclassifiedTag.objects.create(tag_id=tag);

            return HttpResponse('Tag created successfully', status=200);
        except Exception as e:
            print(e);
            return HttpResponse('Bad Request', status=400);
    else:
        return HttpResponse('Unsupported method', status=405);

@login_required
def create_new_post(request):
    if request.method == 'POST':
        try:
            obj = request.POST;

            ## POST

            post = Post();
        
            # Author User

            user = request.user;
        
            post.author_user_id = user;
        
            # Recipe Name

            post.recipe_name = obj['recipe_name'];
        
            # Body (Instructions)

            post.body_text = obj['instructions'];
        
            # Visibility

            raw_visibility = obj['visibility'];
        
            visibility = -1;

            if (raw_visibility == 'public'):
                visibility = 0;
            elif (raw_visibility == 'followers_only'):
                visibility = 1;
            elif (raw_visibility == 'private'):
                visibility = 2;
            else:
                raise Exception('Invalid visibility value');
    
            post.visibility = visibility;

            post.save();

            ## POST INGREDIENTES
            ingredients = obj['ingredients'].split(',');
        
            if not ingredients[0] == '':
                for i in ingredients:
                    ingredient_exists = Ingredient.objects.filter(name=i).exists()
                    if ingredient_exists:
                        ingredient = Ingredient.objects.get(name=i);
                        PostIngredients.objects.create(ingredient_id=ingredient, post_id=post);
                    else:
                        PostIngredients.objects.filter(post_id=post).delete();
                        raise Exception('Invalid ingredients');
                    
        
            ## POST TAGS

            tags = obj['tags'].split(',');
        
            if not tags[0] == '':
                for t in tags:
                    tag_exists = Tag.objects.filter(name=t).exists();
                    if tag_exists:
                        tag = Tag.objects.get(name=t);
                        TagPost.objects.create(post_id=post, tag_id=tag);
                    else:
                        TagPost.objects.filter(post_id=post).delete();
                        raise Exception('Invalid tags');
    
            return HttpResponse('Post created successfully', status=200);
            
        except Exception as e:
            print(e);
            return HttpResponse('Bad Response', status=400);
    else:
        return HttpResponse('Unsupported method', status=405);
            
### /////////// ###



### Edit Post ###
@login_required
def edit_post(request):
    if request.method == 'POST':
        try:
                
            obj = request.POST;
        
            # Post

            post_id = obj['post_id'];
            post = Post.objects.get(id=post_id);
        
            # User 

            user = request.user;
        
            if not user.groups.first().name == 'admin':
                if not user == post.author_user_id:
                    return HttpResponse('Forbidden', status=403);


            # Recipe Name

            post.recipe_name = obj['recipe_name'];

            # Body (Instructions)

            post.body_text = obj['instructions'];
            
            # Visibility

            raw_visibility = obj['visibility'];

            visibility = -1;

            if (raw_visibility == 'public'):
                visibility = 0;
            elif (raw_visibility == 'followers_only'):
                visibility = 1;
            elif (raw_visibility == 'private'):
                visibility = 2;
            else:
                raise Exception('Invalid visibility value');

            post.visibility = visibility;
        

            # Post Ingredients

            in_request_ingredients = obj['ingredients'].split(',');

            current_ingredients = list(PostIngredients.objects.filter(post_id=post).values_list('ingredient_id__name', flat=True));
        
            delete_ingredients = [];
        
            # Identify what ingredients are going to be deleted
            for i in current_ingredients:
                if i not in in_request_ingredients:
                    delete_ingredients.append(i);
        


            # Assign the new ingredients to the Recipe/Post
            for i in in_request_ingredients:
                if not PostIngredients.objects.filter(Q(ingredient_id__name=i) & Q(post_id=post)).exists():
                    if Ingredient.objects.filter(name=i).filter():
                        ingredient = Ingredient.objects.get(name=i);
                        PostIngredients.objects.create(ingredient_id=ingredient, post_id=post);
        
            # Delete ingredients from recipe
            for i in delete_ingredients:
                ingredient = PostIngredients.objects.get(Q(ingredient_id__name=i) & Q(post_id=post));
                ingredient.delete();

            # Post Tags


            in_request_tags = obj['tags'].split(',');

            current_tags = list(TagPost.objects.filter(post_id=post).values_list('tag_id__name', flat=True));
        
            delete_tags = [];
        
            # Identify what tags are going to be deleted
            for t in current_tags:
                if t not in in_request_tags:
                    delete_tags.append(t);
        

            # Assign the new tags to the Recipe/Post
            for t in in_request_tags:
                if not TagPost.objects.filter(Q(tag_id__name=t) & Q(post_id=post)).exists():
                    if Tag.objects.filter(name=t).filter():
                        tag = Tag.objects.get(name=t);
                        TagPost.objects.create(tag_id=tag, post_id=post);
        
            # Delete tags from recipe
            for t in delete_tags:
                tag = TagPost.objects.get(Q(tag_id__name=t) & Q(post_id=post));
                tag.delete();

            post.save();
        
            return HttpResponse('Post has been successfully update', status=200);
        except Exception as e:
            print(e);
            return HttpResponse('An error has ocurred', status=400);
    else:
        return HttpResponse('Unsupported method', status=405);


@login_required
def delete_post(request):
    if request.method == 'POST':
        try:
            obj = request.POST;
        
            if not Post.objects.filter(id=obj['post_id']).exists():
                raise Exception('Such post does not exist');
    
            user = request.user;
            
            post = Post.objects.get(id=obj['post_id']);

            if not user.groups.first().name == 'admin':
                if not post.author_user_id == user:
                    return HttpResponse('Forbidden', status=403);             
    
            post.delete();
        
            return HttpResponse('Post deleted successfully', status=200);     
            
        except Exception:
            return HttpResponse('Bad Request', status=405);     
    else:
        return HttpResponse('Unsupported method', status=405); 

### //////// ###



### Home Page ###

@login_required
def add_remove_like_post(request):
    if request.method == 'POST':
        try:

            obj = request.POST;
            
            user = request.user;
        
            post_id = obj['post_id'];

            post = Post.objects.get(id=post_id);
        
            if not PostLike.objects.filter(Q(user_id=user) & Q(post_id=post)):
                PostLike.objects.create(user_id=user, post_id=post);
            
                return HttpResponse('Like added', status=250);
            else:
                like = PostLike.objects.get(Q(user_id=user) & Q(post_id=post));
                like.delete();
        
                return HttpResponse('Like removed', status=251);

        except Exception as e:
            print(e);
            return HttpResponse('Bad Request', status=400);
    else:
        return HttpResponse('Unsupported method', status=405);

@login_required
def increment_post_seed(request):
    if request.method == 'POST':
        try:
            user = request.user;

            post_seed = PostSeed.objects.get_or_create(user_id=user)[0];
        
            post_seed.seed = post_seed.seed + 1;

            post_seed.save();
        
            return HttpResponse('Post seed incremented successfully', status=200);
        except Exception as e:
            print(e);
            return HttpResponse('An error has ocurred', status=400);
            
    else:
        return HttpResponse('Unsupported method', status=405);

@login_required
def reset_posts(request):
    if request.method == 'POST':
        try:
            user = request.user;

            post_seed = PostSeed.objects.get_or_create(user_id=user)[0];
        
            post_seed.seed = 0;

            post_seed.save();
        
            return HttpResponse('Post seed reset successfully', status=200);
        except Exception as e:
            print(e);
            return HttpResponse('An error has ocurred', status=400);
    else:
        return HttpResponse('Unsupported method', status=405);