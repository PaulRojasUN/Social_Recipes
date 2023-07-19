from django.http import HttpResponse
from .models import FollowingUser, CustomUser, admin_access, priviliged_access, Tag, ClassifiedTag, UnclassifiedTag
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import Group
from django.db.models import Q


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