from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, password_validation, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import ListView

from .forms import RegistrationForm, EditProfileForm, UpdateContactForm, ChangePasswordForm
from .models import Contact

# Create your views here.

def home(request):
    contacts = []
    if request.user.is_authenticated:
        contacts = Contact.objects.filter(user=request.user)
    
    return render(request=request, template_name='home.html', context={"contacts": contacts})

def not_logged_in(request):
    return render(request, 'login_required.html')

def about(request):
    return render(request=request, template_name='about.html', context={})

# don't call login as will clash with core login method
def login_user(request): 

    username = ''
    # determine what request is being received
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        remember_me = request.POST.get('remember_me', False)

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            messages.success(request, "You have been logged in", extra_tags="alert alert-success alert-dismissible fade show")
            return redirect('home')
     
        else:
            messages.error(request, message="Invalid login.  Please try again.", extra_tags="alert alert-danger alert-dismissible fade show text-center")

    return render(request, 'authenticate/login.html', {'username': username})

# @login_required()
def logout_user(request): 

    if request.user.is_authenticated:
        logout(request)

        messages.success(request, "You have been logged out successfully", extra_tags="alert alert-success alert-dismissible fade show")
    return redirect('home')


def register_user(request): 

    # determine what request is being received
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(request, username=username, password=password)
            login(request, user)
        
            messages.success(request, "You have successfully registered and been logged in", extra_tags="alert alert-success alert-dismissible fade show")
            return redirect('home')
        
    else:
        form = RegistrationForm()

    return render(request, 'authenticate/register.html', {'form': form})

@login_required()
def edit_profile(request): 

    # if request.user.is_authenticated:
    # determine what request is being received
    if request.method == "POST":
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
        
            messages.success(request, "You have successfully updated your profile", extra_tags="alert alert-success alert-dismissible fade show")
            return redirect('home')
        
    else:
        form = EditProfileForm(instance=request.user)

    return render(request, 'authenticate/edit_profile.html', {'form': form})
    
    # else :
    #     messages.error(request, "You must be logged in to access that page!", extra_tags="alert alert-danger alert-dismissible fade show")
    #     return redirect('home')


@login_required()
def change_password(request):
    
    # if request.user.is_authenticated:
    # determine what request is being received
    if request.method == "POST":
        form = ChangePasswordForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, "You have successfully updated your password", extra_tags="alert alert-success alert-dismissible fade show")
            return redirect('home')
        
    else:
        form = ChangePasswordForm(user=request.user)

    return render(request, 'authenticate/change_password.html', {'form': form})
    # else :
    #     messages.error(request, "You must be logged in to access that page!", extra_tags="alert alert-danger alert-dismissible fade show")
    #     return redirect('home')


@login_required()
def contact(request, id):
    # if request.user.is_authenticated:
    # contact = get_object_or_404(Contact, id=id, user=request.user)
    contact = get_object_or_404(Contact, id=id)
    form = UpdateContactForm(request.POST or None, request.FILES or None, instance=contact)

    # check user has access
    if request.user == contact.user:
        if form.is_valid():
            form.save()
            messages.success(request, f"{contact} was successfully updated.", extra_tags="alert alert-success alert-dismissible fade show")
            print(f"contact:{contact.image}")
            return redirect('home')
        return render(request=request, template_name='contact.html', context={"contact": contact, 'form':form})
    
    else :
        messages.error(request, "You do not have access to that contact!", extra_tags="alert alert-danger alert-dismissible fade show")
        return redirect('home')

    # else :
    #     messages.error(request, "You must be logged in to access that page!", extra_tags="alert alert-danger alert-dismissible fade show")
    #     return redirect('home')


@login_required()
def add_contact(request):
    if request.user.is_authenticated:
        form = UpdateContactForm(request.POST or None, request.FILES or None)
        
        if form.is_valid():
            toBeSaved = form.save(commit=False)
            toBeSaved.user = request.user
            toBeSaved.save()
            messages.success(request, f"A new contact was successfully added.", extra_tags="alert alert-success alert-dismissible fade show")
            return redirect('home')

        return render(request=request, template_name='contact.html', context={'form': form})
    else :
        messages.error(request, "You must be logged in to access that page!", extra_tags="alert alert-danger alert-dismissible fade show")
        return redirect('home')


@login_required()
def delete_confirmation(request, id):
    # if request.user.is_authenticated:
    # contact = get_object_or_404(Contact, id=id, user=request.user)
    contact = get_object_or_404(Contact, id=id)
    
    if request.user == contact.user:
        if request.method == 'POST':
            # delete the contact from the database
            contact.delete()
            # redirect to the home
            return redirect('home')

    
        return render(request,
                    'delete_confirmation.html',
                    {'name': contact})
    else :
        messages.error(request, "You do not have access to that contact!", extra_tags="alert alert-danger alert-dismissible fade show")
        return redirect('home')
    # else :
    #     messages.error(request, "You must be logged in to access that page!", extra_tags="alert alert-danger alert-dismissible fade show")
    #     return redirect('home')
    