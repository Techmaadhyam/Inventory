from django.urls import path
from core_app import views

urlpatterns = [
    path('', views.Login.as_view(), name="login"),
    path('signup', views.Registration.as_view(), name='signup'),
    path('logout', views.Logout.as_view(), name='logout'),
    path('home', views.Home.as_view(), name='home'),
    path('user-detail', views.user_detail, name="user-detail"),
    path('search-warehouse/', views.search_warehouse, name = 'search_warehouse'),
    path('update_password', views.ChangePassword.as_view(), name='update_password'),
    path('send-forget-password-email', views.SendForgetPasswordEmail.as_view(), name='send-forget-password-email'),
    path('reset-password/<str:token>', views.ResetForgetPassword.as_view(), name='reset-password'),


]
