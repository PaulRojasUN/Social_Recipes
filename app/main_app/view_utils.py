from django.http import HttpResponse, JsonResponse
from .models import FollowingUser, CustomUser
from django.db.models import Q
from django.contrib.auth.models import Group

### View Account ###

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

def predict_username(request, username):
    if request.method == 'GET':
        predicted_usernames = list(CustomUser.objects.filter(username__contains=username).values_list('username', flat=True)[:20]);

        return JsonResponse(predicted_usernames, safe=False);
    else:
        return HttpResponse('Unsupported method', status=405);

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


def add_remove_moderator(request):
    if request.method == 'POST':
        try:
            obj = request.POST;
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


### //////////////////////////////////////////// ####