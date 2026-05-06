from django.contrib import messages
from django.contrib.auth import (
    authenticate,
    login,
    logout,
    password_validation,
    update_session_auth_hash,
)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect, render

from ..forms import ChangePasswordForm, EditProfileForm, RegistrationForm


# don't call login as will clash with core login method
def login_user(request):

    username = ""
    # determine what request is being received
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        remember_me = request.POST.get("remember_me", False)

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            messages.success(
                request,
                "You have been logged in",
                extra_tags="alert alert-success alert-dismissible fade show",
            )
            return redirect("home")

        else:
            messages.error(
                request,
                message="Invalid login.  Please try again.",
                extra_tags="alert alert-danger alert-dismissible fade show text-center",
            )

    return render(request, "authenticate/login.html", {"username": username})


def logout_user(request):

    if request.user.is_authenticated:
        logout(request)

        messages.success(
            request,
            "You have been logged out successfully",
            extra_tags="alert alert-success alert-dismissible fade show",
        )

    return redirect("home")


def register_user(request):

    # determine what request is being received
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password1"]
            user = authenticate(request, username=username, password=password)
            login(request, user)

            messages.success(
                request,
                "You have successfully registered and been logged in",
                extra_tags="alert alert-success alert-dismissible fade show",
            )
            return redirect("home")

    else:
        form = RegistrationForm()

    return render(request, "authenticate/register.html", {"form": form})


@login_required()
def edit_profile(request):

    # determine what request is being received
    if request.method == "POST":
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()

            messages.success(
                request,
                "You have successfully updated your profile",
                extra_tags="alert alert-success alert-dismissible fade show",
            )
            return redirect("home")

    else:
        form = EditProfileForm(instance=request.user)

    return render(request, "authenticate/edit_profile.html", {"form": form})


@login_required()
def change_password(request):

    # determine what request is being received
    if request.method == "POST":
        form = ChangePasswordForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(
                request,
                "You have successfully updated your password",
                extra_tags="alert alert-success alert-dismissible fade show",
            )
            return redirect("home")

    else:
        form = ChangePasswordForm(user=request.user)

    return render(request, "authenticate/change_password.html", {"form": form})
