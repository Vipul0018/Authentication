
from django.urls import path
from account.views import UserRegister,UserLogin,UserProfile,UserChagePass,SendEmailResetPass,UserPassReset
urlpatterns = [
    path('register/',UserRegister.as_view(),name='register'),
    path('login/',UserLogin.as_view(),name='login'),
    path('profile/',UserProfile.as_view(),name='Profile'),
    path('changepass/',UserChagePass.as_view(),name='changepass'),
    path('send-resetpass/',SendEmailResetPass.as_view(),name='resetpass'),
    path('resetpass/<uid>/<token>/',UserPassReset.as_view(),name='resetpass'),
    

]

