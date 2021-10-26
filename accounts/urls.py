from django.urls import path
from . import views

urlpatterns = [
    path('register', views.register),
    path('', views.home),

    path('login', views.login),
    path('logout', views.logout),

    path('adminlogin', views.adminlogin),
    path('adminlogout', views.adminlogout),

    path('adminpage', views.admin),

    path('create_user', views.create_user),
    path('display_user', views.display_user),
    path('update_user', views.update_user),
    path('delete_user', views.delete_user),

    path('add_category', views.add_category),
    path('display_category', views.display_category),
    path('update_category', views.update_category),
    path('delete_category', views.delete_category),

    path('add_product', views.add_product),
    path('display_product', views.display_product),
    path('update_product', views.update_product),
    path('delete_product', views.delete_product),

    path('placed_orders', views.placed_orders),
]
