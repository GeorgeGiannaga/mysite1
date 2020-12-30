from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('', views.register, name='register'),
    path('login', views.log_in, name='log_in'),
    path('home', views.home, name='home'),
    path('new_search', views.new_search, name='new_search'),
    path('properties', views.proper, name='proper'),
    path('logout', views.logoutuser, name='logoutuser'),
    path('reset_password', auth_views.PasswordResetView.as_view(template_name="accounts/password_reset.html"), name="password_reset"),
    path('reset_password_sent', auth_views.PasswordResetDoneView.as_view(template_name="accounts/password_reset_sent.html"), name="password_reset_done"),
    path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name="accounts/password_reset_form.html"), name="password_reset_confirm"),
    path('reset_password_complete', auth_views.PasswordResetCompleteView.as_view(template_name="accounts/password_reset_done.html"), name="password_reset_complete"),
    path('My_properties.pdf', views.render_pdf_view, name="pdfile"),
    path('properviews', views.ProperVeiw, name="properviews"),
    path('editproper/<int:id>', views.editproper, name = 'editproper'),
    path('delete/<int:id>', views.deleteproper, name = 'delproper' )
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
