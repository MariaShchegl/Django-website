from django.shortcuts import redirect
from frontend.forms import AuthForm, RegForm, RecipeForm, ImageForm, CommentForm
from django.contrib.auth import login, logout
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404
from .models import Recipe, Image, Comment
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

import logging
import os

logger = logging.getLogger(__name__)

# Create your views here.

# Store a newly created resource in storage.
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def store(request):
    form = RecipeForm(data=request.POST)
    formIm = ImageForm(request.POST, request.FILES)
    if form.is_valid() and len(request.FILES) and formIm.is_valid():
        image = formIm.save()
        Recipe.objects.create(image=image, description=form.data['description'], title=form.data['title'], user=request.user)
        return HttpResponse('success')
    else:
        if len(form.errors) > 0 and not form.is_valid():
            response = form.errors
            response.update(formIm.errors)
            return JsonResponse(response.as_json(), safe=False, status=400)
        elif len(form.errors) > 0:
            return JsonResponse(form.errors.as_json(), safe=False, status=400)
        else:
            return JsonResponse(formIm.errors.as_json(), safe=False, status=400)


# Update the specified resource in storage.
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update(request, id=0):
    recipe = get_object_or_404(Recipe, id=id, user=request.user)
    form = RecipeForm(data=request.data, instance=recipe)
    if form.is_valid():
        form.save()
        image = Image.objects.get(id=recipe.image.id)
        formIm = ImageForm(request.data, request.FILES, instance=image)
        if formIm.is_valid() and len(request.FILES):
            image_path = image.pathImage.path
            if os.path.exists(image_path):
                try:
                    os.remove(image_path)
                except PermissionError:
                    pass
            formIm.save()
        return HttpResponse('success')
    else:
        return JsonResponse(form.errors.as_json(), safe=False, status=400)


# Remove the specified resource from storage.
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def remove(request, id=0):
    recipe = get_object_or_404(Recipe, id=id, user=request.user)
    image_path = recipe.image.pathImage.path
    if os.path.exists(image_path):
        os.remove(image_path)
    recipe.image.delete()
    recipe.delete()
    return redirect('account')


# Login user
@api_view(['POST'])
def signin(request):
    form = AuthForm(data = request.POST)
    if form.is_valid():
        user = form.get_user()
        login(request, user)
        return HttpResponse('success')
    else:
        return JsonResponse(form.errors.as_json(), safe=False, status=401)


# Add comment
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_comment(request, id=0):
    form = CommentForm(data=request.POST)
    if form.is_valid():
        user = request.user
        recipe = get_object_or_404(Recipe, id=id)
        Comment.objects.create(user=user, recipe=recipe, data=form.data['data'])
        return redirect('/recipe/' + str(id))
    else:
        return redirect('index')


# Register user
@api_view(['POST'])
def signup(request):
    form = RegForm(data = request.POST)
    if form.is_valid():
        user = form.save()
        login(request, user)
        return HttpResponse('success')
    else:
        return JsonResponse(form.errors.as_json(), safe=False, status=401)


# Logout user
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def logout_my(request):
    logout(request)
    return redirect('index')