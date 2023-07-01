from app_auth import views
from django.urls import path

urlpatterns = [
    path('signup/', views.signup, name ='signup'),
    path('signin/', views.signin, name ='signin'),
    path('signout/', views.signout, name ='signout'),
    path('activate/<uidb64>/<token>', views.ActivateAccountView.as_view(), name ='activate'),
    path('request-reset-email/', views.RequestResetEmailView.as_view(), name ='request-reset-email'),
    path('set-new-passwd/<uidb64>/<token>', views.SetNewPasswordView.as_view(), name ='set-new-passwd'),
    ]