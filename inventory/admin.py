from django.contrib import admin
from .models import Inventory, Category, Warehouse, Rack
# Register your models here.

admin.site.register(Inventory)
# admin.site.register(Category)
# admin.site.register(Warehouse)
# admin.site.register(Rack)

@admin.register(Warehouse)
class WarehouseModelAdmin(admin.ModelAdmin):
    list_display =['id','user','name','address','description']

@admin.register(Category)
class CategoryModelAdmin(admin.ModelAdmin):
    list_display =['id','user','name']

@admin.register(Rack)
class RackModelAdmin(admin.ModelAdmin):
    list_display =['id','user','rack']

