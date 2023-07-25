from django.contrib import admin

from .models import Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['parent', 'title', 'created_time', 'avatar']
    list_filter = ['parent']
    search_fields = ['title']
