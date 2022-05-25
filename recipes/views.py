from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, 'recipes/index.html', {'categories': [1, 2, 3, 4], 'popPosts': [1, 2, 3]})
