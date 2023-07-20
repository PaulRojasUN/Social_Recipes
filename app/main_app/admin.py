from django.contrib import admin

# User imports 
from .models import CustomUser, FollowingUser

# Tags imports
from .models import Tag, ClassifiedTag, UnclassifiedTag, TagUser

# Ingredients imports
from .models import Ingredient, ClassifiedIngredient, UnclassifiedIngredient

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



