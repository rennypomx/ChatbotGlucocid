from django.urls import path
from . import views
from .views import UserDetailView

urlpatterns = [
    path('', views.index, name='index'),
    path('inicio/', views.inicio, name='inicio'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),  # Nueva ruta para cerrar sesión
    path('api/user/', UserDetailView.as_view(), name='api_user_detail'),
]
