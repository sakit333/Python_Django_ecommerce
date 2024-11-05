from django.urls import path
from . import views

urlpatterns = [
    path('register/',views.RegisterView.as_view(),name='register'),
    path('signin/',views.SigninView.as_view(),name='signin'),
    path('',views.HomeView.as_view(),name='home'),
    path('signout/',views.SignoutView.as_view(),name='signout'),
    path('reset_password/<str:username>',views.ResetPasswordView.as_view(),name='resetpassword'),
    path('forgot_password/',views.ForgotPasswordView.as_view(),name='forgotpassword'),
    path('sample/',views.SampleView.as_view(),name='sample'),
    path('product/<str:slug>',views.ProductView.as_view(),name='product'),
    
    path('product/<str:sizename>/<str:slug>',views.SelectsizeView.as_view(),name='selectsize'),
    path('addtocart/<str:slug>/<str:size>/<str:category>',views.add_to_cart,name='addtocart'),
    path('cart/',views.cart,name='cart'),
    path('incrementquantity/<int:id>',views.increment_quantity,name='increment'),
    path('decrementquantity/<int:id>',views.decrement_quantity,name='decrement'),
    path('remove/<int:id>',views.remove_orderitem,name='remove'),



    # path('payment/', views.PaymentView.as_view(), name='payment'),
    path('orders/', views.OrdersView.as_view(), name='orders'),
    path('payment/',views.Pymentview.as_view(),name='payment'),
    path('checkout/',views.Checkoutview.as_view(),name='checkout')
]
   
    
