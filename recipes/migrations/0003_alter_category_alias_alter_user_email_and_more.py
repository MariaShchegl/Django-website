# Generated by Django 4.0.4 on 2022-05-26 11:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_remove_image_path_remove_recipe_data_image_pathimage_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='alias',
            field=models.CharField(max_length=30, unique=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.CharField(max_length=30, unique=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='login',
            field=models.CharField(max_length=30, unique=True),
        ),
    ]
