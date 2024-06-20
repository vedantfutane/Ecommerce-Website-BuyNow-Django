from django.conf import settings
from . import views
from django.urls import path
from django.conf.urls.static import static
from django.contrib.auth import views as auth_view
from .forms import LoginForm
from .forms import MyPasswordResetForm,MyPasswordChangeForm,MySetPasswordForm


urlpatterns =[
    path("",views.home,name="home"),
    path('upcoming/',views.upcoming,name="upcoming"),
    path('about/',views.about,name="about"),
    path('contact/',views.contact,name="contact"),
    path("shop/<slug:val>",views.ShopView.as_view(),name="shop"),
    path('accounts/profile/',views.ProfileView.as_view(),name="profile"),
    path('accounts/address/',views.address,name="address"),
    path('updateAddress/<int:pk>',views.updateAddress.as_view(),name="updateAddress"),
    
    path('add-to-cart/',views.add_to_cart,name='add-to-cart'),
    path('cart/',views.show_cart,name='showcart'),
    path('checkout/',views.checkout.as_view(),name='checkout'),
    path('paymentdone/',views.payment_done,name='paymentdone'),
    path('orders/',views.home,name='orders'),
    
    
    path('pluscart/',views.plus_cart),
    path('minuscart/',views.minus_cart),
    path('removecart/',views.remove_cart),
    
    #login authentication urls get here
    path('registration/',views.CustomerRegistrationView.as_view(),name="customerregistration"),
    path('accounts/login/',auth_view.LoginView.as_view(template_name='myapp/login.html',authentication_form=LoginForm),name='login'),
    path('passwordchange/',auth_view.PasswordChangeView.as_view(template_name='myapp/changepassword.html',form_class=MyPasswordChangeForm,success_url='/passwordchangedone'),name='passwordchange'),    
    path('passwordchangedone/',auth_view.PasswordChangeDoneView.as_view(template_name='myapp/passwordchangedone.html'),name='passwordchangedone'),
    
    #Logout is built in function in auth_view  so no need to create in views file
    path('logout/',auth_view.LogoutView.as_view(next_page='login'),name='logout'),
    
    #for forgot password needed
    path('password-reset/',auth_view.PasswordResetView.as_view(template_name='myapp/password_reset.html',form_class=MyPasswordResetForm),name="password_reset"),
    path('password-reset/done/',auth_view.PasswordResetDoneView.as_view(template_name='myapp/password_reset_done.html'),name="password_reset_done"),
    path('password-reset-confirm/<uidb64>/<token>/',auth_view.PasswordResetConfirmView.as_view(template_name='myapp/password_reset_confirm.html',form_class=MySetPasswordForm),name="password_reset_confirm"),
    path('password-reset-complete/',auth_view.PasswordResetCompleteView.as_view(template_name='myapp/password_reset_complete.html'),name="password_reset_complete"),
    
    
    ]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
