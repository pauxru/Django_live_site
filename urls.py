from django.urls import path
from . import views
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView

urlpatterns = [
    path('', views.index, name='index'),
    path('aboutus/',views.aboutus, name='aboutus'),
    path('contactus/',views.contactus,name='contactus'),
    path('signup/',views.register,name='signup'),
    path('login/',views.login,name='login'),
    path('register/',views.register,name='register'),
    path('make_payment/',views.make_payment,name='make_payment'),
    path('feedback/', views.feedback, name='feedback'),
    path('login_user/', views.login_user, name='login_user'),
    path('password_reset/', views.password_reset, name='password_reset'),
    path('logout_user/', views.logout_user, name='logout_user'),
    path('profile/', views.profile, name='profile'),
    path('change_password/', views.change_password, name='change_password'),
    path('home/', views.home, name='home'),
    path('favicon.ico', RedirectView.as_view(url=staticfiles_storage.url('img/favicon.ico'))),
    path('accounts/deposit/',views.deposit,name='deposit'),
    path('accounts/transactions/',views.transactions,name='transactions'),
    path('products/buy_airtime/',views.buy_airtime,name='buy_airtime'),
    path('products/surveys/',views.surveys,name='surveys'),
    path('accounts/referral_earnings/',views.referral_earnings,name='referral_earnings'),
    path('support/contact_us/',views.send_message,name='send_message'),
    path('statement/',views.statements,name='statement'),
    path('support/notifications/',views.notifications,name='notifications'),
    path('withdraw_earnings/',views.withdraw_earnings,name='withdraw_earnings'),
    path('terms_and_conditions/',views.terms_and_conditions,name='terms_and_conditions'),
    path('privacy_policy',views.privacy_policy,name='privacy_policy'),
    path('terms/',views.terms,name='terms'),
    path('privacy/',views.privacy,name='privacy')
]