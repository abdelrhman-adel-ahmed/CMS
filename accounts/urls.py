from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import  views as auth_views

urlpatterns = [
    path('',views.Home.as_view(),name="home"),
    path('product/',views.product.as_view(),name="product"),
    path('customer/<str:id>/',views.customer.as_view(),name="customer"),
    path('customer_list/',views.customer_list.as_view(),name="customer_list"),
    path('createorder/<str:id>/',views.CreateOrder.as_view(),name="createorder"),
    path('createcustomer/',views.CreateCustomer.as_view(),name="createcustomer"),
    path('update_order/<str:id>/',views.UpdateOrder.as_view(),name="update_order"),
    path('delete_order/<str:id>/',views.DeleteOrder.as_view(),name="delete_order"),
    path('register/',views.Register.as_view(),name="register"),
    path('login/',views.Login.as_view(),name="login"),
    path('logout/',views.Logout.as_view(),name="logout"),
    path('user/',views.User.as_view(),name="user"),
    path('User_Setting/',views.User_Setting.as_view(),name="User_Setting"),
    path('reset_password/',auth_views.PasswordResetView.as_view
    (template_name='accounts/password_reset.html'),
    name="password_reset"),
    path('password-reset_sent/',auth_views.PasswordResetDoneView.as_view
    (template_name='accounts/password_reset_done.html'),
    name="password_reset_done"),
    path('reset-password-confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view
    (template_name='accounts/password_reset_confirm.html'),
    name="password_reset_confirm"),
    path('reset-password-complete/',auth_views.PasswordResetCompleteView.as_view
    (template_name='accounts/password_reset_complete.html'),
    name="password_reset_complete"),
]


if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)