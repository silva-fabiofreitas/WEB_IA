from django.contrib import admin
from .models import MindMap, Category

@admin.register(MindMap)
class MindMapAdmin(admin.ModelAdmin):
    ...

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    ...


