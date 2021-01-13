from django.contrib import admin
from blog import models
from django_summernote.admin import SummernoteModelAdmin


class SomeModelAdmin(SummernoteModelAdmin):  # instead of ModelAdmin
    summernote_fields = 'text'


admin.site.register(models.Profile)

admin.site.register(models.Post, SomeModelAdmin)

admin.site.register(models.Comment)


