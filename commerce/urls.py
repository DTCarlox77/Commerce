from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', main, name='main'),
    path('auctions/', auctions, name='auctions'),
    path('new_product/', new_product, name='new_product'),
    path('product/<int:id>', product, name='product'),
    path('category/', auctions, name='category'),
    path('login/', login, name='login'),
    path('sign_in/', login, name='sign_in'),
    path('search/', auctions, name='search'),
    path('comment/<int:id>', comment, name='comment')
]
