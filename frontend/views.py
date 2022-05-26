from django.shortcuts import render

# Create your views here.

# Display a listing of the resource.
# GET
def index(request):
    return render(request, 'frontend/index.html', {'categories': [1, 2, 3, 4], 'popPosts': [1, 2, 3]})

# Show the form for creating a new resource.
# GET
# isAuth
def create(request):
    pass

# Display the specified resource.
# GET
def show(request, id):
    return render(request, 'frontend/recipe.html')

# Show the form for editing the specified resource.
# GET
# isAuth
def edit(request, id):
    pass