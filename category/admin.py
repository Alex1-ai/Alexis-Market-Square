from django.contrib import admin
from .models import Category, Market
# Register your models here.


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ["category_name"]}
    list_display = ['category_name', 'slug',
                    'cart_image', 'created_at', 'updated_at']


@admin.register(Market)
class MarketAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ["market_name"]}
    list_display = ['market_name', 'slug',
                    'market_image', 'created_at', 'updated_at']
