from django.shortcuts import redirect
from frontend.forms import AuthForm, RegForm
from django.contrib.auth import login, logout
from django.http import JsonResponse, HttpResponse

import json
import logging

logger = logging.getLogger(__name__)

# Create your views here.

# Store a newly created resource in storage.
# POST
# isAuth
def store(request):
    pass

# Update the specified resource in storage.
# PUT
# isAuth
def update(request, id=1):
    pass

# Remove the specified resource from storage.
# DELETE
# isAuth
def remove(request, id=1):
    pass

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