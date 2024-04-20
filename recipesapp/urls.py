from django.urls import path
from . import views 
from django.conf import settings
from django.conf.urls.static import static

app_name = 'recipesapp'

urlpatterns = [
    path('', views.home, name='home'),
    path('recipe/<int:recipe_id>/', views.recipe_detail, name='recipe_detail'),
    path('recipe/add/', views.add_recipe, name='add_recipe'),
    path('recipe/edit/<int:recipe_id>/', views.edit_recipe, name='edit_recipe'),
    path('recipe/del/<int:recipe_id>/', views.delete_recipe, name='delete_recipe'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.register, name='register'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)