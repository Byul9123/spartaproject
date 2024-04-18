from django.urls import path , include
from . import views

app_name = 'accounts'
urlpatterns = [
    path('profile/<str:username>/', views.profile, name = 'profile'),
    path('login/', views.login, name = 'login'),
    path('logout/', views.logout, name = 'logout'),
    path('signup/', views.signup, name = 'signup'),
    path('delete/', views.delete, name = 'delete'),
    path('update/', views.update, name = 'update'),
    path('password/', views.password, name = 'password'),
    path('<int:user_id>/follow/', views.follow, name = 'follow'),
]
