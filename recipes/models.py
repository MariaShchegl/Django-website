from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class TextFieldImpl(models.TextField):
    "Implements comma-separated storage of lists"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def db_type(self, connection):
        return 'TEXT'

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()

        return name, path, args, kwargs

class Image(models.Model):
    pathImage = models.ImageField()

class Recipe(models.Model):
    title = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = TextFieldImpl(default="")
    image = models.OneToOneField(Image,
        on_delete=models.CASCADE)
    def __str__(self):
        return self.title
    class Meta:
        indexes = [
            models.Index(fields=['created_at'], name='recipe_idx'),
        ]

class Category(models.Model):
    title = models.CharField(max_length=30)
    alias = models.CharField(max_length=30, unique=True)
    recipe = models.ManyToManyField(Recipe, null=True, blank=True)
    def __str__(self):
        return self.title
    class Meta:
        indexes = [
            models.Index(fields=['id'], name='category_idx'),
        ]

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    data = TextFieldImpl(default="")
    def __str__(self):
        return self.data
    class Meta:
        indexes = [
            models.Index(fields=['created_at'], name='comment_idx'),
        ]
