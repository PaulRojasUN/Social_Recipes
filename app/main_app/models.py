# @name: models.py
# @description: Models are defined in this file
# @author: Paul Rodrigo Rojas G.
# @email: paul.rojas@correounivalle.edu.co, PaulRodrigoRojasECL@gmail.com


from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
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




### Tag ###

class Tag(models.Model):
    name = models.CharField(max_length=64);

    def __str__(self):
        return self.name;
 
class ClassifiedTag(models.Model):
    tag_id = models.ForeignKey('Tag', on_delete=models.CASCADE);

class UnclassifiedTag(models.Model):
    tag_id = models.ForeignKey('Tag', on_delete=models.CASCADE);

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

class ClassifiedIngredient(models.Model):
    ingredient_id = models.ForeignKey('Ingredient', on_delete=models.CASCADE);

class UnclassifiedIngredient(models.Model):
    ingredient_id = models.ForeignKey('Ingredient', on_delete=models.CASCADE);

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
