from django.contrib import admin
from .models import *

# Register your models here.

@admin.register(Category, Recipe, Comment, Image)
class author_admin(admin.ModelAdmin):
    pass
