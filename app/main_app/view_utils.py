from django.http import HttpResponse, JsonResponse
from .models import FollowingUser, CustomUser, admin_access, Tag, ClassifiedTag, priviliged_access, TagUser
from django.db.models import Q
from django.contrib.auth.decorators import login_required, user_passes_test

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



@user_passes_test(priviliged_access)
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
            
            return JsonResponse(obj);
        except Exception as e:
            print(e);
            return HttpResponse('Bad request', status=400);
    else:
        return HttpResponse('Unsupported method', status=405);

########################


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