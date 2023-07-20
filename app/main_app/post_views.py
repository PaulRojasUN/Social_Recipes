from django.http import HttpResponse
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth.models import Group
from django.db.models import Q

# User 
from .models import FollowingUser, CustomUser

# Tags
from .models import Tag, ClassifiedTag, UnclassifiedTag, TagUser

# Access
from .models import priviliged_access, admin_access 

# Ingredients

from .models import Ingredient, ClassifiedIngredient, UnclassifiedIngredient

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