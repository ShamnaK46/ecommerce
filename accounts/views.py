from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.models import auth
from .forms import *
from .models import Product, Category
from ecommerce.models import Order, CartProduct
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from .decorators import *

# Create your views here.

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def login(request):
    if request.method == 'POST':
        username = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            request.session['username'] = username
            return JsonResponse(
                {'success': True},
                safe=False)
        else:
            return JsonResponse(
                {'success': False},
                safe=False)
    else:
        return render(request, 'userlogin.html')


def register(request):
    if request.method == 'POST':
        email = request.POST['email']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        password = request.POST['password']
        print(email)
        user = User.objects.create_user(
            username=email, last_name=last_name, first_name=first_name, password=password, email=email)
        user.save()
        return JsonResponse(
            {'success': True},
            safe=False)
    return render(request, 'register.html')


def home(request):
    product = Product.objects.all()
    return render(request, 'home.html', {'products': product})


@login_required(login_url='/login')
def logout(request):
    auth.logout(request)
    return redirect("/home")


@superuser_required
def admin(request):
    return render(request, 'admin.html')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def adminlogin(req):
    if req.method == 'POST':
        username = req.POST['email']
        password = req.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(req, user)
            return JsonResponse(
                {'success': True},
                safe=False)
        else:
            return JsonResponse(
                {'success': False},
                safe=False)
    return render(req, 'adminlogin.html')


@superuser_required
def adminlogout(request):
    return render(request, 'adminlogin.html')


@superuser_required
def create_user(request):
    if request.method == 'POST':
        email = request.POST['email']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        password = request.POST['password']
        print(email)
        user = User.objects.create_user(
            username=email, last_name=last_name, first_name=first_name, password=password, email=email)
        user.save()
        return JsonResponse(
            {'success': True},
            safe=False)
    return render(request, 'create_user.html')


@superuser_required
def display_user(request):
    users = User.objects.all()
    return render(request, 'display_user.html', {'users': users})


@superuser_required
def update_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        u = User.objects.get(username=username)
        if u is not None:
            if email != '':
                u.username = email
            if first_name != '':
                u.first_name = first_name
            if last_name != '':
                u.last_name = last_name
            u.save()
            return JsonResponse(
                {'success': True},
                safe=False)
        else:
            return JsonResponse(
                {'success': True},
                safe=False)
    return render(request, 'update_user.html')


@superuser_required
def delete_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        u = User.objects.get(username=username)
        if u is not None:
            u.delete()
            return JsonResponse(
                {'success': True},
                safe=False)
        else:
            return JsonResponse(
                {'success': True},
                safe=False)
    return render(request, 'delete_user.html')


@superuser_required
def add_category(request):
    if request.method == 'POST':
        category = request.POST['category']
        cat = Category.objects.create(name=category)
        cat.save()
        return JsonResponse(
            {'success': True},
            safe=False)
    return render(request, 'add_category.html')


@superuser_required
def update_category(request):
    if request.method == 'POST':
        category = request.POST['category']
        newcategory = request.POST['newcategory']
        c = Category.objects.get(name=category)
        if c is not None:
            c.name = newcategory
            c.save()
            return JsonResponse(
                {'success': True},
                safe=False)
        else:
            return JsonResponse(
                {'success': True},
                safe=False)
    return render(request, 'update_category.html')


@superuser_required
def display_category(request):
    category = Category.objects.all()
    return render(request, 'display_category.html', {'categories': category})


@superuser_required
def delete_category(request):
    if request.method == 'POST':
        category = request.POST['category']
        c = Category.objects.get(name=category)
        if c is not None:
            c.delete()
            return JsonResponse(
                {'success': True},
                safe=False)
        else:
            return JsonResponse(
                {'success': True},
                safe=False)
    return render(request, 'delete_category.html')


@superuser_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()

        return redirect('/adminpage')
    form = ProductForm()
    return render(request, 'add_product.html', {'form': form})


@superuser_required
def delete_product(request):
    if request.method == 'POST':
        name = request.POST['product']
        p = Product.objects.get(name=name)
        if p is not None:
            p.delete()
            return JsonResponse(
                {'success': True},
                safe=False)
        else:
            return JsonResponse(
                {'success': True},
                safe=False)
    return render(request, 'delete_product.html')


@superuser_required
def update_product(request):
    if request.method == 'POST':
        prodname = request.POST['prodname']
        name = request.POST['name']
        quantity = request.POST['quantity']
        category = request.POST['category']
        price = request.POST['price']
        description = request.POST['description']
        p = Product.objects.get(name=prodname)
        if p is not None:
            if name != '':
                p.name = name
            if name != '':
                p.quantity = quantity
            if category != '':
                p.category_id = category
            if price != '':
                p.price = price
            if description != '':
                p.description = description
            p.save()
        return JsonResponse(
            {'success': True},
            safe=False)
    cat = Category.objects.all()
    return render(request, 'update_product.html', {'categories': cat})


@superuser_required
def display_product(request):
    product = Product.objects.all()
    return render(request, 'display_product.html', {'products': product})


@superuser_required
def placed_orders(req):
    order = Order.objects.all()
    orderedproduct = CartProduct.objects.all()
    product = Product.objects.all()
    return render(req, "placed_orders.html", {"orders": order, "orderedproducts": orderedproduct, "products": product})
