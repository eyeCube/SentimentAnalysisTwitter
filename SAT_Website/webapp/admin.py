from django.contrib import admin

from .models import Email


@admin.register(Email)
class EmailAdmin(admin.ModelAdmin):
    list_display = ['name', 'Email', 'EmailSent']


"""
Other models have not been added to Django's admin panel because of their extent,
thus being easier to manage through a dedicated MySQL program.
"""
