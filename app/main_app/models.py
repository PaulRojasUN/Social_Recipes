# @name: models.py
# @description: Models are defined in this file
# @author: Paul Rodrigo Rojas G.
# @email: paul.rojas@correounivalle.edu.co, PaulRodrigoRojasECL@gmail.com


from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db.models.signals import post_migrate, post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group


import uuid


### User ###

class CustomUserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError("The username must be set")
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)   
        extra_fields.setdefault('first_name', 'Admin')
        return self.create_user(username, password, **extra_fields)



class CustomUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False);

    USERNAME_FIELD = 'username';

    objects = CustomUserManager()

    def __str__(self):
        return self.username;


class FollowingUser(models.Model):
    follower_user_id = models.ForeignKey(CustomUser, related_name='main_app_following_user_follower_user', on_delete=models.CASCADE);
    target_user_id = models.ForeignKey(CustomUser, related_name='main_app_following_user_target_user', on_delete=models.CASCADE);

    def __str__(self):
        return 'Follower: ' + str(self.follower_user_id.first_name) + ' - ' + 'Target: ' + str(self.target_user_id.first_name);

### ////////////// ###


### User Groups ###

@receiver(post_migrate)
def create_users_groups(sender, **kwargs):
    users_groups = ["regular_users", "moderators", "admin"];
    for g in users_groups:
        if not Group.objects.filter(name=g).exists():
            new_group = Group(name=g);
            new_group.save();

@receiver(post_save, sender=CustomUser)
def Add_Person_To_Clients(sender, instance, created, **kwargs):
    if created:
        if instance.is_staff == True and instance.is_superuser == True:
            group_name = "admin";
        else:
            group_name = "regular_users";
        
        if Group.objects.filter(name=group_name).exists():
                group = Group.objects.get(name=group_name);
                instance.groups.add(group);
        else:
            print("User could not be added to admin gruop");


def priviliged_access(user):
    try:
        if (user.is_authenticated):
            group_name = user.groups.first().name;

            if group_name == 'moderators' or group_name == 'admin':
                return True;
            else:
                raise Exception('Forbidden');
        else:
            raise Exception('Login required');
    except Exception:
        return False


def admin_access(user):
    try:
        if (user.is_authenticated):

            group_name = user.groups.first().name;

            if group_name == 'admin':
                return True;
            else:
                raise Exception('Forbidden');
        else:
            raise Exception('Login required');
    except Exception:
        return False
    


### //////////////// ###



### Tag ###

class Tag(models.Model):
    name = models.CharField(max_length=64, unique=True);

    def __str__(self):
        return self.name;
 
class ClassifiedTag(models.Model):
    tag_id = models.ForeignKey('Tag', on_delete=models.CASCADE);

    def __str__(self):
        return str(self.tag_id.name);

class UnclassifiedTag(models.Model):
    tag_id = models.ForeignKey('Tag', on_delete=models.CASCADE);
    
    def __str__(self):
        return str(self.tag_id.name);

class TagIngredient(models.Model):
    tag_id = models.ForeignKey('Tag', on_delete=models.CASCADE);
    ingredient_id = models.ForeignKey('Ingredient', on_delete=models.CASCADE);

class TagPost(models.Model):
    tag_id = models.ForeignKey('Tag', on_delete=models.CASCADE);
    post_id = models.ForeignKey('Post', on_delete=models.CASCADE);

class TagUser(models.Model):
    tag_id = models.ForeignKey('Tag', on_delete=models.CASCADE);
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE);
    
    def __str__(self):
        return 'Tag: ' + str(self.tag_id.name) + ' - User: ' + str(self.user_id.first_name);


### ////////////// ###





### Ingredient ###

class Ingredient(models.Model):
    name = models.CharField(max_length=64);

    def __str__(self):
        return self.name;

class ClassifiedIngredient(models.Model):
    ingredient_id = models.ForeignKey('Ingredient', on_delete=models.CASCADE);

    def __str__(self):
        return str(self.ingredient_id.name);

class UnclassifiedIngredient(models.Model):
    ingredient_id = models.ForeignKey('Ingredient', on_delete=models.CASCADE);

    def __str__(self):
        return str(self.ingredient_id.name);

### ////////////// ###




### Post ### 

class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False);
    author_user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE);
    recipe_name = models.CharField(max_length=64);
    body_text = models.TextField();
    visibility = models.SmallIntegerField();
    post_date = models.DateField(); 

class PostIngredients(models.Model):
    ingredient_id = models.ForeignKey('Ingredient', on_delete=models.CASCADE);
    post_id = models.ForeignKey('Post', on_delete=models.CASCADE);


class PostLike(models.Model):
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE);
    post_id = models.ForeignKey('Post', on_delete=models.CASCADE);
    
### ////////////// ###
