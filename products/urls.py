from django.urls import path , include
from . import views

app_name = "products"
urlpatterns = [
    path('', views.products, name = 'products'),
    path('create/', views.create, name = 'create'),
    path('<int:pk>/', views.detail, name = 'detail'),
    path('delete/<int:pk>/', views.delete, name = 'delete'),
    path('update/<int:pk>/', views.update, name = 'update'),
    path ('<int:pk>/like/', views.like, name = 'like'),
    
]
