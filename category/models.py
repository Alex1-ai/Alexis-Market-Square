from django.db import models
from django.urls import reverse
# Create your models here.


class Market(models.Model):
    market_name = models.CharField(max_length=60, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    title = models.CharField(max_length=255)
    is_active = models.BooleanField(default=False)
    description = models.TextField(blank=True)
    market_image = models.ImageField(upload_to='photos/markets')
    created_at = models.DateTimeField(auto_now_add=True, )
    updated_at = models.DateTimeField(auto_now=True)

    # class Meta:
    #     verbose_name = 'market'
    #     verbose_name_plural = 'markets'

    def get_url(self):
        return reverse('categories_by_market', args=[self.slug])

    def __str__(self):
        return self.market_name



class Category(models.Model):
    category_name = models.CharField(max_length=60, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField()
    cart_image = models.ImageField(upload_to='photos/categories')
    market = models.ForeignKey(Market, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, )
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def get_url(self):
        return reverse('products_by_category', args=[self.slug])

    def __str__(self):
        return self.category_name
