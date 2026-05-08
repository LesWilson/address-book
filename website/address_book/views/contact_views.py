from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from ..forms import UpdateContactForm
from ..models import Contact


@login_required()
def contact(request, id):
    contact = get_object_or_404(Contact, id=id)

    # check user has access
    if request.user == contact.user:
        form = UpdateContactForm(
            request.POST or None, request.FILES or None, instance=contact
        )
        if form.is_valid():
            toBeSaved = form.save(commit=False)
            toBeSaved.updated_by = request.user
            toBeSaved.save()

            messages.success(
                request,
                f"{contact} was successfully updated.",
                extra_tags="alert alert-success alert-dismissible fade show",
            )
            return redirect("home")

        return render(
            request=request,
            template_name="contact.html",
            context={"contact": contact, "form": form},
        )

    else:
        messages.error(
            request,
            "You do not have access to that contact!",
            extra_tags="alert alert-danger alert-dismissible fade show",
        )
        return redirect("home")


@login_required()
def add_contact(request):
    if request.user.is_authenticated:
        form = UpdateContactForm(request.POST or None, request.FILES or None)

        if form.is_valid():
            toBeSaved = form.save(commit=False)
            toBeSaved.user = request.user
            toBeSaved.created_by = request.user
            toBeSaved.updated_by = request.user
            toBeSaved.save()
            messages.success(
                request,
                f"A new contact was successfully added.",
                extra_tags="alert alert-success alert-dismissible fade show",
            )
            return redirect("home")

        return render(
            request=request, template_name="contact.html", context={"form": form}
        )
    else:
        messages.error(
            request,
            "You must be logged in to access that page!",
            extra_tags="alert alert-danger alert-dismissible fade show",
        )
        return redirect("home")


@login_required()
def delete_confirmation(request, id):
    contact = get_object_or_404(Contact, id=id)

    if request.user == contact.user:
        if request.method == "POST":
            # delete the contact from the database
            contact.delete()
            # redirect to the home
            return redirect("home")

        return render(request, "delete_confirmation.html", {"name": contact})
    else:
        messages.error(
            request,
            "You do not have access to that contact!",
            extra_tags="alert alert-danger alert-dismissible fade show",
        )
        return redirect("home")


def search(request):
    contacts = []
    if request.user.is_authenticated:
        search_string = request.GET["search_string"]
        contacts = Contact.objects.filter(
            Q(user=request.user)
            & (
                Q(first_name__icontains=search_string)
                | Q(last_name__icontains=search_string)
            )
        )

    return render(
        request=request, template_name="home.html", context={"contacts": contacts}
    )
