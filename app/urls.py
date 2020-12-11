from django.urls import path
from .import views
from django.conf.urls import url


urlpatterns = [

    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerPage, name="register"),
    url(r'^$', views.home, name='home'),
    url(r'^products/(?P<id>[0-9]+)/$', views.product_detail, name='product_detail'),
    url(r'create_product/', views.create_product, name='create_product'),
    url(r'^my_products/$', views.my_products, name='my_products'),
    url(r'^edit_product/(?P<id>[0-9]+)/$', views.edit_product, name='edit_product'),
    url(r'^profile/(?P<username>\w+)/$', views.profile, name="profile"),
    url(r'^checkout/$', views.make_purchase, name="make_purchase"),
    url(r'^my_sales/$', views.my_sales, name='my_sales'),
    url('my_purchases/', views.my_purchases, name='my_purchases'),
    url(r'^category/(?P<link>[\w|-]+)/$', views.category, name="category"),
    url(r'^search/$', views.search, name='search'),
]
