from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import update_session_auth_hash, get_user_model
from django.views.decorators.http import require_http_methods, require_POST
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from products.models import Product
from .models import User
from .forms import CustomUserChangeForm, CustomUserCreationForm
from django.contrib.auth.decorators import login_required
# Create your views here.
def profile(request, username):
    member = get_object_or_404(get_user_model(), username=username)
    products = Product.objects.all().order_by('-pk')
    user = request.user.pk
    likes = Product.objects.filter(like_users__pk=user)
    context = {
        "member": member,
        "user": user,
        "products": products,
        "likes": likes
    }
    return render(request, "accounts/profile.html", context)

@require_http_methods(['GET', 'POST'])
def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            next_url = request.GET.get('next') or 'index'
            return redirect(next_url)
    else:
        form = AuthenticationForm()
        context = {
            'form' : form
        }
        return render(request, 'accounts/login.html', context)
    
@require_POST
def logout(request):
    if request.method == 'POST':
        auth_logout(request)
    return redirect('index')

@require_http_methods(['GET', 'POST'])
def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user =form.save()
            auth_login(request, user)
            return redirect('index')

    else:
        form =CustomUserCreationForm()
    context = {'form' : form}
    return render(request, 'accounts/signup.html', context)

@require_POST
def delete(request):
    if request.user.is_authenticated:
        request.user.delete()
        auth_logout(request)
    return redirect('index')

@require_http_methods(['GET', 'POST'])
def update(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = CustomUserChangeForm(instance=request.user)
    context = {
        'form' : form
    }
    return render(request, 'accounts/update.html', context)

@login_required
@require_http_methods(['GET', 'POST'])
def password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('index')
    else:
        form = PasswordChangeForm(request.user)
    context = {
        'form' : form
    }
    return render(request, 'accounts/password.html', context)

@require_POST
def follow(request, user_id):
    if request.user.is_authenticated:
        member = get_object_or_404(get_user_model(), pk=user_id)
        if request.user != member:
            if request.user in member.followers.all():
                member.followers.remove(request.user)
            else:
                member.followers.add(request.user)
        return redirect("accounts:profile", member.username)
    return redirect("accounts:login")