import os
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login, logout,authenticate
from .forms import RecipeForm
from .models import Recipe,RecipeCategoryRelationship,Category
from django.contrib.auth.decorators import login_required
from django.contrib import messages 
from datetime import datetime


def home(request):
    categories = Category.objects.all()
    recipe_relationships = RecipeCategoryRelationship.objects.all().order_by('-id')[:5]
    return render(request, 'recipesapp/home.html', {'categories': categories, 'recipe_relationships': recipe_relationships})

def recipe_detail(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    return render(request, 'recipesapp/recipe_detail.html', {'recipe': recipe})

#Авторизация
def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Добро пожаловать, {username}!')
                return redirect('recipesapp:home')
            else:
                messages.error(request, 'Некорректные логин или пароль.')
    else:
        form = AuthenticationForm()
    return render(request, 'recipesapp/login.html', {'form': form})

#Разлогинивание
def user_logout(request):
    logout(request)
    return redirect('recipesapp:home')

#Регистрация
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Аккаунт создан для {username}!')
            return redirect('recipesapp:login')
    else:
        form = UserCreationForm()
    return render(request, 'recipesapp/register.html', {'form': form})

#Создание рецепта
@login_required(login_url='/accounts/login/')  
def add_recipe(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.image = request.FILES['image']
            
            current_time = datetime.now().strftime("%Y%m%d%H%M%S%f")
            file_extension = recipe.image.name.split('.')[-1]
            file_name = f"{current_time}.{file_extension}"
            recipe.image.name = file_name
            recipe.save()

            category_id = request.POST.get('category')
            category = Category.objects.get(pk=category_id)
            RecipeCategoryRelationship.objects.create(recipe=recipe, category=category)            
            return redirect('recipesapp:home')
    else: 
        form = RecipeForm()
    return render(request, 'recipesapp/add_recipe.html', {'form': form})    

#Редактирование рецепта
def edit_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    recipe_category_relationship = RecipeCategoryRelationship.objects.filter(recipe=recipe).first()
    previous_category = None

    if recipe_category_relationship:
        previous_category = recipe_category_relationship.category

    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES, instance=recipe)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            
            if 'image' in request.FILES:
                recipe.image = request.FILES['image']
                current_time = datetime.now().strftime("%Y%m%d%H%M%S%f")
                file_extension = recipe.image.name.split('.')[-1]
                file_name = f"{current_time}.{file_extension}"
                recipe.image.name = file_name

            recipe.save()

            category_id = request.POST.get('category')
            if category_id:
                category = Category.objects.get(pk=category_id)
            else:
                category = previous_category

            if recipe_category_relationship:
                recipe_category_relationship.category = category
                recipe_category_relationship.save()
            else:
                RecipeCategoryRelationship.objects.create(recipe=recipe, category=category)

            return redirect('recipesapp:home')
    else:
        form = RecipeForm(instance=recipe)
    
    return render(request, 'recipesapp/edit_recipe.html', {'form': form})

# Удаление рецепта
# def delete_recipe(request, recipe_id):
#     recipe = get_object_or_404(Recipe, id=recipe_id)
#     recipe.delete()
#     return redirect('recipesapp:home')

def delete_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    
    # Удаление файла из папки recipe_image
    if recipe.image:
        image_path = recipe.image.path
        if os.path.exists(image_path):
            os.remove(image_path)
    
    recipe.delete()
    
    return redirect('recipesapp:home')
