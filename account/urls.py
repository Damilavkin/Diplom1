from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from . import views
from .views import profile_list,profile_detail


app_name = "account"
urlpatterns = [
    # url-адреса входа и выхода
    # path('login/', auth_views.LoginView.as_view(), name='login'),
    # path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    ## url-адреса смены пароля
    # path('password-change/', auth_views.PasswordChangeView.as_view(),
    #     name='password_change'),
    # path('password-change/done/', auth_views.PasswordChangeDoneView.as_view(),
    #     name='password_change_done'),
    ## url - сброса пароля
    # path('password-reset/', auth_views.PasswordResetView.as_view(),
    #     name='password_reset'),
    # path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    # path('password-reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(),
    #     name='password_reset_confirm'),
    # path('password-reset/complete/', auth_views.PasswordResetCompleteView.as_view(),
    #     name='password_reset_complete'),
    path('', include('django.contrib.auth.urls')),  # url для встроенных вьюшек аутентификаций
    path('', views.dashboard, name='dashboard'),
    path('register/', views.register, name='register'),
    path('edit/', views.edit, name='edit'),
    path('profiles/', profile_list, name='profile_list'),
    path('profiles/<str:username>/', profile_detail, name='profile_detail'),
    path('token_login/', views.token_login, name='token_login'),


]
