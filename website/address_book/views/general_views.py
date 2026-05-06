from django.shortcuts import render

from ..models import Contact


def home(request):
    contacts = []
    if request.user.is_authenticated:
        contacts = Contact.objects.filter(user=request.user)

    return render(
        request=request, template_name="home.html", context={"contacts": contacts}
    )


def not_logged_in(request):
    return render(request, "login_required.html")


def about(request):
    return render(request=request, template_name="about.html", context={})
