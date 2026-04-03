from django.contrib import admin

from .models import Product, Variation, ReviewRating, ProductGallery
import admin_thumbnails
# Register your models here.


@admin_thumbnails.thumbnail('image')
class ProductGalleryInline(admin.TabularInline):
    model = ProductGallery
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ["product_name"]}
    list_display = ['product_name', 'slug',
                    'price', 'image', 'stock', 'category', 'is_available', 'created_date', 'modified_date']
    inlines = [ProductGalleryInline]


@admin.register(Variation)
class VariationAdmin(admin.ModelAdmin):
    list_display = ['product', 'variation_category',
                    'variation_value', 'is_active', 'created_date', 'updated_date']
    list_filter = ['product', 'variation_category',
                   'variation_value']
    list_editable = ['is_active']


@admin.register(ReviewRating)
class ReviewRatingAdmin(admin.ModelAdmin):
    # prepopulated_fields = {'slug': ["product_name"]}
    list_display = ['product', 'user', 'rating',
                    'subject', 'ip', 'status', 'created_at', 'updated_at']


admin.site.register(ProductGallery)
