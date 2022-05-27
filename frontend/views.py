from django.shortcuts import render
from .forms import AuthForm, RegForm
from recipes.models import Category, Image, Comment, Recipe
from django.core.paginator import Paginator

# Create your views here.

# Display a listing of the resource.
# GET

def index(request):
    categories = Category.objects.all().order_by('title')
    pop_posts = Recipe.objects.all()[:3]
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

# Show the form for creating a new resource.
# GET
# isAuth
def create(request):
    pass

# Display the specified resource.
# GET
def show(request, id=1):
    categories = Category.objects.all()
    pop_posts = Recipe.objects.all()[:3]

    recipe = Recipe.objects.filter(id=id).first()

    context = {'categories': categories, 'popPosts': pop_posts, 'recipe': recipe}

    if request.user.is_authenticated:
        context['user'] = request.user
        return render(request, 'frontend/recipe.html', context)
    else:
        context['regForm'] = RegForm()
        context['form'] = AuthForm()
        return render(request, 'frontend/recipe.html', context)

# Show the form for editing the specified resource.
# GET
# isAuth
def edit(request, id=1):
    pass