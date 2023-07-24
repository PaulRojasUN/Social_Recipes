from django.contrib import admin

# User imports 
from .models import CustomUser, FollowingUser

# Tags imports
from .models import Tag, ClassifiedTag, UnclassifiedTag, TagUser, TagPost

# Ingredients imports
from .models import Ingredient, ClassifiedIngredient, UnclassifiedIngredient

# Posts imports
from .models import Post, PostIngredients, PostLike, PostSeed

# User
admin.site.register(CustomUser);
admin.site.register(FollowingUser);

# Tags
admin.site.register(Tag);
admin.site.register(ClassifiedTag);
admin.site.register(UnclassifiedTag);
admin.site.register(TagUser);

# Ingredients
admin.site.register(Ingredient);
admin.site.register(ClassifiedIngredient);
admin.site.register(UnclassifiedIngredient);

# Post
admin.site.register(Post);
admin.site.register(PostIngredients);
admin.site.register(PostLike);
admin.site.register(TagPost);
admin.site.register(PostSeed);
