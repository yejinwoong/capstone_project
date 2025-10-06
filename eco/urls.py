from django.contrib import admin
from django.urls import path
from shop.views import home, dashboard, product_list, cart, add_to_cart  # ← 존재하는 것만

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('dashboard/', dashboard, name='dashboard'),
    path('products/', product_list, name='products'),
    path('cart/', cart, name='cart'),
    path('add/', add_to_cart, name='add'),
]
