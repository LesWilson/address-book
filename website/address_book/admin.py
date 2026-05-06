from django.contrib import admin
from .models import Contact

class ContactAdmin(admin.ModelAdmin):
    list_display = ["first_name", "last_name", "email"]
    list_filter = ["last_name"]
    readonly_fields = ["user"]

admin.site.register(Contact, ContactAdmin)