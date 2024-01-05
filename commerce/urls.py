from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', main, name='main'),
    path('auctions/', auctions, name='auctions'),
    path('new_product/', new_product, name='new_product'),
    path('product/<int:id>', product, name='product'),
    path('products/', user_products, name='user_products'),
    path('watch_list', watch_list, name='watch_list'),
    path('add_remove_list/<int:id>', add_remove_list, name='add_remove_list'),
    path('bid/<int:id>', bid, name='bid'),
    path('close_auction/<int:id>', close_auction, name='close_auction'),
    path('category/<str:filtro>', category, name='category'),
    path('comment/<int:id>', comment, name='comment'),
    path('login/', login, name='login'),
    path('sign_in/', sign_in, name='sign_in'),
    path('close', close, name='close')
]
