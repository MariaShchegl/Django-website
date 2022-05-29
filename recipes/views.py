from django.shortcuts import redirect
from frontend.forms import AuthForm, RegForm, RecipeForm, ImageForm
from django.contrib.auth import login, logout
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404
from .models import Recipe, Image
from rest_framework.decorators import api_view

import logging
import os

logger = logging.getLogger(__name__)

# Create your views here.

# Store a newly created resource in storage.
# POST
# isAuth
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
            return JsonResponse(response.as_json(), safe=False)
        elif len(form.errors) > 0:
            return JsonResponse(form.errors.as_json(), safe=False)
        else:
            return JsonResponse(formIm.errors.as_json(), safe=False)


# Update the specified resource in storage.
# PUT
# isAuth
@api_view(['PUT'])
def update(request, id):
    recipe = get_object_or_404(Recipe, id=id, user=request.user)
    form = RecipeForm(data=request.data, instance=recipe)
    if form.is_valid():
        form.save()
        image = Image.objects.get(id=recipe.image.id)
        formIm = ImageForm(request.data, request.FILES, instance=image)
        if formIm.is_valid() and len(request.FILES):
            image_path = image.pathImage.path
            if os.path.exists(image_path):
                os.remove(image_path)
            formIm.save()
        return HttpResponse('success')
    else:
        return JsonResponse(form.errors.as_json(), safe=False)


# Remove the specified resource from storage.
# DELETE
# isAuth
@api_view(['GET'])
def remove(request, id=1):
    recipe = get_object_or_404(Recipe, id=id, user=request.user)
    image_path = recipe.image.pathImage.path
    if os.path.exists(image_path):
        os.remove(image_path)
    recipe.image.delete()
    recipe.delete()
    return redirect('account')


# Login user
# POST
def signin(request):
    form = AuthForm(data = request.POST)
    if form.is_valid():
        user = form.get_user()
        login(request, user)
        return HttpResponse('success')
    else:
        return JsonResponse(form.errors.as_json(), safe=False)


# Register user
# POST
def signup(request):
    form = RegForm(data = request.POST)
    if form.is_valid():
        user = form.save()
        login(request, user)
        return HttpResponse('success')
    else:
        return JsonResponse(form.errors.as_json(), safe=False)


# Logout user
# GET
# isAuth
def logOut(request):
    logout(request)
    return redirect('index')