from django.shortcuts import get_object_or_404, render, redirect
from .models import Product
from .forms import ProductForm
from django.views.decorators.http import require_http_methods, require_POST
from django.contrib.auth.decorators import login_required
# Create your views here.
def index(request):
    return render(request, 'products/index.html')

def products(request):
    products = Product.objects.all().order_by('-pk')
    context = {
        'products' : products
    }
    return render(request, 'products/products.html', context)

@login_required
@require_http_methods(['GET', 'POST'])
def create(request):
    if request.method == 'POST':        
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.author = request.user
            product.save()
            return redirect('products:detail', product.pk)
    else:
        form = ProductForm() 
        context = {
            'form' : form
        }   
        return render(request, 'products/create.html', context)
def detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    context = {
        'product' : product
    }
    return render(request, 'products/detail.html', context)

@login_required
@require_POST
def delete(request, pk):
    if request.user.is_authenticated:
        product = get_object_or_404(Product, pk=pk)
        product.delete()
    return redirect('products:products')


@require_http_methods(['GET', 'POST'])
def update(request, pk):
    products = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=products)
        if form.is_valid():
            product =form.save()
            return redirect('products:detail', product.pk)
    else:
        form = ProductForm(instance=products)
        context = {
            'form' : form,
            'product' : products
        }
        return render(request, 'products/update.html', context)
    
@require_POST
def like(request, pk):
    if request.user.is_authenticated:        
        product = get_object_or_404(Product, pk=pk)
        if product.like_users.filter(pk=request.user.pk).exists():
            product.like_users.remove(request.user)
            return redirect('products:detail', product.pk)
        else:
            product.like_users.add(request.user)
            return redirect('products:detail', product.pk)
    return redirect('accounts:login')

