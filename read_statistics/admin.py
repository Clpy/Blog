from django.contrib import admin
from .models import ReadNum


# Register your models here.
@admin.register(ReadNum)
class ReadNumAdmin(admin.ModelAdmin):
    list_display = (
        'content_object',
        'content_type',
        'read_num',
    )