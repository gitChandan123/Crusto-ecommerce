"""
URL configuration for Restaurant_project project.
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from Base_App.views import *
from django.contrib.auth.views import LogoutView,LoginView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', homeView,name='Home'),
    path('book_table/', login_required(bookTableView), name='Book_Table'),
    path("booking-success/", booking_success, name="Booking_Success"),
    path('menu/', menuView,name='Menu'),
    path('about/', aboutView,name='About'),
    path('feedback/', login_required(feedbackView), name='Feedback_Form'),
    path('login/', LoginView.as_view(template_name='login.html'), name='User_Login'),
    path('register/', user_register,name="User_Register"),
    path('user_profile/<int:user_id>/',login_required(user_profile),name="User_Profile"),
    path('logout/', LogoutView.as_view(next_page='User_Login'), name='logout'),
    path('search/',search,name="Search"),
    # cart section and their routes
    path('cart/',cart_view,name='cart'),
    path('add-to-cart/<int:product_id>/',add_to_cart,name='add_to_cart'),
    path('update_cart/<int:product_id>/', update_cart, name='update_cart'),
    path('increase_cart/<int:product_id>/', increase_quantity, name='increase_quantity'),
    path('decrease_cart/<int:product_id>/', decrease_quantity, name='decrease_quantity'),
    path('remove_from_cart/<int:product_id>/',remove_from_cart, name='remove_from_cart'),
    path('create-checkout-session/', create_checkout_session, name='create_checkout_session'),
    path('buy-now/<int:product_id>/',buy_now,name='buy_now'),
    path('success/',success,name="success"),
    path('cancel/',cancel,name="cancel"),
    # Address route
    path('add_address/',add_address,name="add_address"),    
    path('delete_address/<int:address_id>/',delete_address,name="delete_address"),
    path('item_details/<int:product_id>',item_details,name="item_details"),
    path('add_review/<int:product_id>',add_review,name="add_review"),
    path('edit_review/<int:review_id>/', edit_review, name='update_review'),
    path('delete_review/<int:review_id>/', delete_review, name='delete_review'),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

