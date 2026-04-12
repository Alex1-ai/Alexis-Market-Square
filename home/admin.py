from django.contrib import admin
from .models import Contact, NewsletterSubscription
from . import models
# Register your models here.

# Register your models here.
admin.site.site_header = 'ALEXIS-MARKT'
admin.site.index_title = 'ALEXIS Admin'
# admin.site.index_title = 'Admin'

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):

    list_display = ['contact_name', 'email',
                    'subject', 'created_at', 'updated_at']


@admin.register(NewsletterSubscription)
class NewsletterSubscriptionAdmin(admin.ModelAdmin):
    list_display = ['email', 'subscribed_at']


@admin.register(models.FrequentQuestion)
class FrequentQuestionAdmin(admin.ModelAdmin):
    list_display = ['question', 'answer', 'number', ]


@admin.register(models.SupportStaffDetails)
class SupportStaffDetailsAdmin(admin.ModelAdmin):
    list_display = ['location', 'email', 'contact',
                    'open_hours', 'twitter_link', 'facebook_link', 'instagram_link', 'linkedin_link']


@admin.register(models.Testimonies)
class TestimoniesAdmin(admin.ModelAdmin):
    list_display = ['name', 'job_title', 'rating',
                    'customer_review', 'is_accepted', 'created_at', 'updated_at']


@admin.register(models.HomePageWords)
class HomePageWordsAdmin(admin.ModelAdmin):
    list_display = ['logo', 'title', 'subtitle']



@admin.register(models.Features)
class FeaturesAdmin(admin.ModelAdmin):
    list_display = ['featureName', 'featureIcon']
