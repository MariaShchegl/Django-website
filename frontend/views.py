from django.shortcuts import render
from .forms import AuthForm, RegForm, RecipeForm, CommentForm
from recipes.models import Category, Image, Comment, Recipe
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

# Create your views here.

@api_view(['GET'])
def index(request):
    '''
        Display a listing of the ricipes.

        show form signup/signin, sidebar (category,
        popular posts), create pagination
    '''

    categories = Category.objects.all().order_by('title')
    pop_posts = Recipe.objects.all()[:3]

    if request.GET.get('category'):
        recipe_list = Recipe.objects.filter(categories=request.GET.get('category'))
    else:
        recipe_list = Recipe.objects.all()
    paginator = Paginator(recipe_list, 3)

    if request.GET.get('page'):
        page_number = request.GET.get('page')
    else:
        page_number = 1

    page_obj = paginator.get_page(page_number)
    list_page = list(paginator.get_elided_page_range(page_number, on_each_side=1))

    context = {'categories': categories, 'popPosts': pop_posts, 'page_obj': page_obj, 'paginationList': list_page}

    if request.user.is_authenticated:
        context['user'] = request.user
        return render(request, 'frontend/index.html', context)
    else:
        context['form'] = AuthForm()
        context['regForm'] = RegForm()
        return render(request, 'frontend/index.html', context)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def create(request):
    '''
        Show the form for creating a new recipe.
    '''

    form = RecipeForm()
    context = {'form': form}
    return render(request, 'frontend/recipe_add.html', context)


@api_view(['GET'])
def show(request, id=1):
    '''
        Display the specified recipe.

        id is the recipe identifier
    '''

    categories = Category.objects.all().order_by('title')
    pop_posts = Recipe.objects.all()[:3]

    recipe = get_object_or_404(Recipe, id=id)

    context = {'categories': categories, 'popPosts': pop_posts, 'recipe': recipe}

    if request.user.is_authenticated:
        context['user'] = request.user
        form = CommentForm()
        context['form'] = form
        return render(request, 'frontend/recipe.html', context)
    else:
        context['regForm'] = RegForm()
        context['form'] = AuthForm()
        return render(request, 'frontend/recipe.html', context)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def edit(request, id):
    '''
        Show the form for editing the specified recipe.

        id is the recipe identifier
    '''

    recipe = get_object_or_404(Recipe, id=id, user=request.user)
    form = RecipeForm(instance=recipe)
    context = {'form': form, 'recipe_id': id}
    return render(request, 'frontend/recipe_edit.html', context)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def account(request):
    '''
        Show account.

        account it is page users after signin
    '''

    recipe_list = Recipe.objects.filter(user=request.user.id)
    paginator = Paginator(recipe_list, 3)

    if request.GET.get('page'):
        page_number = request.GET.get('page')
    else:
        page_number = 1
    page_obj = paginator.get_page(page_number)
    list_page = list(paginator.get_elided_page_range(page_number, on_each_side=1))

    context = {'page_obj': page_obj, 'paginationList': list_page}

    context['user'] = request.user
    return render(request, 'frontend/account.html', context)