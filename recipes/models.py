from django.db import models

# Create your models here.

class User(models.Model):
    login = models.CharField(max_length=30)
    password = models.CharField(max_length=128)
    email = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)

class Image(models.Model):
    path = models.Field()

class Recipe(models.Model):
    title = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    data = models.Field()
    image = models.OneToOneField(Image,
        on_delete=models.CASCADE)
    class Meta:
        indexes = [
            models.Index(fields=['created_at'], name='recipe_idx'),
        ]

class Category(models.Model):
    title = models.CharField(max_length=30)
    alias = models.CharField(max_length=30)
    recipe = models.ManyToManyField(Recipe)
    class Meta:
        indexes = [
            models.Index(fields=['id'], name='category_idx'),
        ]

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    data = models.CharField(max_length=750)
    class Meta:
        indexes = [
            models.Index(fields=['created_at'], name='comment_idx'),
        ]
