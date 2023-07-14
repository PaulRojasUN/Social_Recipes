# @name: models.py
# @description: Models are defined in this file
# @author: Paul Rodrigo Rojas G.
# @email: paul.rojas@correounivalle.edu.co, PaulRodrigoRojasECL@gmail.com


from django.db import models


### Tag ###

class Tag(models.Model):
    name = models.CharField(max_length=64);

    def __str__(self):
        return self.name;


class TagRecipe(models.Model):
    tag_id = models.ForeignKey('Tag', related_name='main_app_tag_recipe_tag_id', on_delete=models.CASCADE);
    recipe_id = models.ForeignKey('Recipe', related_name='main_app_tag_recipe_recipe_id', on_delete=models.CASCADE);

    def __str__(self):
        return "t:" + str(self.tag_id) + " - " + "r:" +  str(self.recipe_id);


class TagIngredient(models.Model):
    tag_id = models.ForeignKey('Tag', related_name='main_app_tag_ingredients_tag_id', on_delete=models.CASCADE);
    ingredient_id = models.ForeignKey('Ingredient', related_name='main_app_tag_ingredients_ingredient_id', on_delete=models.CASCADE);


### --- ###


### Recipe ###

class Recipe(models.Model):
    name = models.CharField(max_length=64);

    def __str__(self):
        return self.name;

### --- ###

### Ingredient ###

class Ingredient(models.Model):
    name = models.CharField(max_length=64);

class ClassifiedIngredient(models.Model):
    ingredient_id = models.ForeignKey('Ingredient', related_name='main_app_classified_ingredient_id', on_delete=models.CASCADE);

class UnclassifiedIngredient(models.Model):
    ingredient_id = models.ForeignKey('Ingredient', related_name='main_app_unclassified_ingredient_id', on_delete=models.CASCADE);
### --- ###


### Post ### 

### --- ###

