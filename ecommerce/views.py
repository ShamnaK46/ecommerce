from django.shortcuts import render, redirect
from accounts.models import Product
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse, request
from .models import *
from django.views.generic import View, TemplateView, CreateView, FormView, DetailView, ListView
from .forms import *



def home(request):
    product = Product.objects.all()
    return render(request, 'home.html', {'products': product})

@login_required(login_url='/login')
def profile(request):
    if request.method == 'POST':
        username = request.session['username']
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
    if request.session.has_key('username'):
        username = request.session['username']
        u = User.objects.get(username=username)
        print(u.first_name)
        if u is not None:
            first_name = u.first_name
            email = u.email
            last_name = u.last_name
            return render(request, 'profile.html', {'fname': first_name, 'lname': last_name, 'email': email})
    return redirect('/home')

@login_required(login_url='/login')
def edit_profile(request):
    if request.method == 'POST':
        username = request.session['username']
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
    return render(request, 'edit_profile.html')


class AddToCartView(TemplateView):
    template_name = "addtocart.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # get product id from requested url
        product_id = self.kwargs['pro_id']
        # get product
        product_obj = Product.objects.get(id=product_id)

        # check if cart exists
        cart_id = self.request.session.get("cart_id", None)
        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id)
            this_product_in_cart = cart_obj.cartproduct_set.filter(
                product=product_obj)

            # item already exists in cart
            if this_product_in_cart.exists():
                cartproduct = this_product_in_cart.last()
                cartproduct.quantity += 1
                cartproduct.subtotal += product_obj.price
                cartproduct.save()
                cart_obj.total += product_obj.price
                cart_obj.save()
            # new item is added in cart
            else:
                cartproduct = CartProduct.objects.create(
                    cart=cart_obj, product=product_obj, rate=product_obj.price, quantity=1, subtotal=product_obj.price)
                cart_obj.total += product_obj.price
                cart_obj.save()

        else:
            cart_obj = Cart.objects.create(total=0)
            self.request.session['cart_id'] = cart_obj.id
            cartproduct = CartProduct.objects.create(
                cart=cart_obj, product=product_obj, rate=product_obj.price, quantity=1, subtotal=product_obj.price)
            cart_obj.total += product_obj.price
            cart_obj.save()

        return context

class MyCartView(TemplateView):
    template_name = "mycart.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_id = self.request.session.get("cart_id", None)
        if cart_id:
            cart = Cart.objects.get(id=cart_id)
        else:
            cart = None
        context['cart'] = cart
        return context

class ManageCartView(View):
    def get(self, request, *args, **kwargs):
        cp_id = self.kwargs["cp_id"]
        action = request.GET.get("action")
        cp_obj = CartProduct.objects.get(id=cp_id)
        cart_obj = cp_obj.cart

        if action == "inc":
            cp_obj.quantity += 1
            cp_obj.subtotal += cp_obj.rate
            cp_obj.save()
            cart_obj.total += cp_obj.rate
            cart_obj.save()
        elif action == "dcr":
            cp_obj.quantity -= 1
            cp_obj.subtotal -= cp_obj.rate
            cp_obj.save()
            cart_obj.total -= cp_obj.rate
            cart_obj.save()
            if cp_obj.quantity == 0:
                cp_obj.delete()

        elif action == "rmv":
            cart_obj.total -= cp_obj.subtotal
            cart_obj.save()
            cp_obj.delete()
        else:
            pass
        return redirect("mycart")

class EmptyCartView(View):
    def get(self, request, *args, **kwargs):
        cart_id = request.session.get("cart_id", None)
        if cart_id:
            cart = Cart.objects.get(id=cart_id)
            cart.cartproduct_set.all().delete()
            cart.total = 0
            cart.save()
        return redirect("mycart")

def productdetails(request):
    if request.method == 'POST':
        id = request.POST['id']
        request.session['p_id'] = id
        return JsonResponse(
                {'success': True},
                safe=False)
    if request.session.has_key('username'):
        id = request.session['p_id']
        product = Product.objects.get(id=id)
        return render(request,"productdetails.html",{"product":product})
    return render(request,"productdetails.html")


class CheckoutView(CreateView):
    template_name = "checkout.html"
    form_class = CheckoutForm
    success_url = "/home"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            pass
        else:
            return redirect("/login/?next=/checkout/")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_id = self.request.session.get("cart_id", None)
        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id)
        else:
            cart_obj = None
        context['cart'] = cart_obj
        return context

    def form_valid(self, form):
        cart_id = self.request.session.get("cart_id")
        username = self.request.session.get("username")
        print(username)
        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id)
            form.instance.cart = cart_obj
            form.instance.subtotal = cart_obj.total
            form.instance.discount = 0
            form.instance.total = cart_obj.total
            form.instance.order_status = "Order Received"
            total = cart_obj.total
            pm = form.cleaned_data.get("payment_method")
            if pm == "PayPal":
                form.save()
                return redirect("/paypalpay")
            del self.request.session['cart_id']
            form.save()
            return redirect("/home")
        else:
            return redirect("/home")
        return super().form_valid(form)


@login_required(login_url='/login')
def Paypalpay(req):
    cart_id = req.session.get("cart_id")
    if cart_id:
        cart_obj = Cart.objects.get(id=cart_id)
        total = cart_obj.total
    else:
        total = 0
    print(total)
    return render(req, "paypal.html", {"total": total})


@login_required(login_url='/login')
def success(req):
    del req.session['cart_id']
    return redirect("/home")


@login_required(login_url='/login')
def productdetails(req):
    if req.method == 'POST':
        id = req.POST['id']
        req.session['p_id'] = id
        return JsonResponse(
            {'success': True},
            safe=False)
    if req.session.has_key('username'):
        id = req.session['p_id']
        product = Product.objects.get(id=id)
        return render(req, "productdetails.html", {"product": product})
    return render(req, "productdetails.html")

@login_required(login_url='/login')
def orders(req):
    username = req.session['username']
    print(username)
    orders = Order.objects.all().filter(u_id=username)
    if orders is not None:
        return render(req,"order_history.html",{"orders":orders})
    return redirect("/home")
