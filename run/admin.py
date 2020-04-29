from django.contrib import admin
from .models import Playbook, Tag, Job


@admin.register(Playbook)
class PlaybookAdmin(admin.ModelAdmin):
    autocomplete_fields = ['tags']


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    search_fields = ['name']

admin.site.register(Job)
