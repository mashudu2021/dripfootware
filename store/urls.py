from django.urls import path, include
from . import views

urlpatterns = [
    
    path('', views.home, name='home'),
    path('shop/', views.shop, name='shop'),
    path('pre-order/', views.preorder, name='pre-order'),
    path('register/', views.register_user, name='register'),
    path('update_user/', views.update_user, name='upadate_user'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('Product/<int:pk>', views.product, name='product'),
    path('about/', views.about, name='about'),
]
