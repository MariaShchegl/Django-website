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

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def store(request):
    '''
        Store a newly created recipe in storage.
    '''

    form = RecipeForm(data=request.POST)
    formIm = ImageForm(request.POST, request.FILES)

    if form.is_valid() and len(request.FILES) and formIm.is_valid():
        image = formIm.save()
        Recipe.objects.create(image=image, description=form.data['description'], title=form.data['title'], user=request.user)

        logging.info('Success add recipe')
        return HttpResponse('success')
    else:
        if len(form.errors) > 0 and not form.is_valid():
            response = form.errors
            response.update(formIm.errors)
            logging.warning('Error valid add(Error valid form and image)')
            return JsonResponse(response.as_json(), safe=False, status=400)
        elif len(form.errors) > 0:
            logging.warning('Error valid add(Error valid image)')
            return JsonResponse(form.errors.as_json(), safe=False, status=400)
        else:
            logging.warning('Error valid add(Error valid form)')
            return JsonResponse(formIm.errors.as_json(), safe=False, status=400)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update(request, id=0):
    '''
        Update the specified recipe in storage.

        id is the recipe identifier for update
    '''

    recipe = get_object_or_404(Recipe, id=id, user=request.user)
    form = RecipeForm(data=request.data, instance=recipe)

    if form.is_valid():
        form.save()

        image = Image.objects.get(id=recipe.image.id)
        image_path = image.pathImage.path
        formIm = ImageForm(request.data, request.FILES, instance=image)

        if formIm.is_valid() and len(request.FILES):
            if os.path.exists(image_path):
                try:
                    os.remove(image_path)
                except PermissionError:
                    pass
            formIm.save()

        logging.info('Success update (user: ' + request.user.username + ', recipe_id: ' + str(id) + ')')
        return HttpResponse('success')
    else:
        logging.warning('Error valid update')
        return JsonResponse(form.errors.as_json(), safe=False, status=400)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def remove(request, id=0):
    '''
        Remove the specified recipe from storage.

        id is the recipe identifier for remove
    '''

    recipe = get_object_or_404(Recipe, id=id, user=request.user)
    image_path = recipe.image.pathImage.path

    if os.path.exists(image_path):
        os.remove(image_path)

    recipe.image.delete()
    recipe.delete()

    logging.info('Success delete recipe ' + str(id))
    return redirect('account')


@api_view(['POST'])
def signin(request):
    '''
        Login user.
    '''

    form = AuthForm(data = request.POST)
    if form.is_valid():
        user = form.get_user()
        login(request, user)

        logging.info('Success login ' + user.username)
        return HttpResponse('success')
    else:
        logging.warning('Error valid login')
        return JsonResponse(form.errors.as_json(), safe=False, status=401)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_comment(request, id=0):
    '''
        Add comment.

        id is the recipe identifier for add comment
    '''

    form = CommentForm(data=request.POST)
    if form.is_valid():
        user = request.user
        recipe = get_object_or_404(Recipe, id=id)
        Comment.objects.create(user=user, recipe=recipe, data=form.data['data'])

        logging.info('Success add comment(user: ' + user.username + ', recipe_id: ' + str(recipe.id) + ')')
        return redirect('/recipe/' + str(id))
    else:
        logging.warning('Error valid add comment')
        return redirect('index')


@api_view(['POST'])
def signup(request):
    '''
        Register user.
    '''

    form = RegForm(data=request.POST)
    if form.is_valid():
        user = form.save()
        login(request, user)

        logging.info('Success register ' + user.username)
        return HttpResponse('success')
    else:
        logging.warning('Error valid register')
        return JsonResponse(form.errors.as_json(), safe=False, status=401)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def logout_my(request):
    '''
        Logout user.
    '''

    logout(request)
    return redirect('index')