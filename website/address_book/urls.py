from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about', views.about, name='about'),

    # path('profile', views.profile, name='profile'),
    path('login', views.login_user, name='login_user'),
    path('logout', views.logout_user, name='logout_user'),
    path('register', views.register_user, name='register_user'),
    path('edit_profile', views.edit_profile, name='edit_profile'),
    path('change_password', views.change_password, name='change_password'),
    path('contact/<int:id>', views.contact, name='contact'),
    # path('delete-contact/<int:id>', views.delete_contact, name='delete_contact'),
    path('delete-contact/<int:id>', views.delete_confirmation, name='delete_contact'),
    path('add-contact', views.add_contact, name='add_contact'),
    # path('delete-confirmation/<int:id>', views.delete_confirmation, name='delete_confirmation'),

    path('login_required', views.not_logged_in, name='login_required'),
]
