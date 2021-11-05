"""ecommerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views
from .views import *
from django.views.static import serve
from django.conf.urls import url

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),
    path('home', views.home),
    path('profile', views.profile),
    path('edit_profile', views.edit_profile),

    path("add-to-cart-<int:pro_id>/", AddToCartView.as_view(), name="addtocart"),
    path("my-cart/", MyCartView.as_view(), name="mycart"),
    path("my-cart/managecart/<int:cp_id>/", ManageCartView.as_view(), name="managecart"),
    path("my-cart/emptycart/", EmptyCartView.as_view(), name="emptycart"),
    path("emptycart/", EmptyCartView.as_view(), name="emptycart"),
    path("productdetails",views.productdetails),

    path("my-cart/checkout/", CheckoutView.as_view(), name="checkout"),
    path("paypalpay/", views.Paypalpay),
    path("paypalpay/success/", views.success),
    path("orders/", views.orders),
    url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    url(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),

]

urlpatterns = urlpatterns + \
              static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
