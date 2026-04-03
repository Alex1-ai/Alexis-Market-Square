from django.db import models

# Create your models here.


class FrequentQuestion(models.Model):
    number = models.IntegerField(unique=True)
    question = models.CharField(max_length=255)
    answer = models.TextField()


class SupportStaffDetails(models.Model):
    location = models.CharField(max_length=288)
    email = models.EmailField()
    contact = models.CharField(max_length=15)
    open_hours = models.CharField(max_length=255)
    twitter_link = models.CharField(max_length=500, null=True, blank=True)
    facebook_link = models.CharField(max_length=500, null=True, blank=True)
    instagram_link = models.CharField(max_length=500, null=True, blank=True)
    linkedin_link = models.CharField(max_length=500, null=True, blank=True)


class Testimonies(models.Model):
    name = models.CharField(max_length=256)
    email = models.EmailField(max_length=254, )
    job_title = models.CharField(max_length=80)
    rating = models.IntegerField()
    customer_review = models.TextField()
    is_accepted = models.BooleanField(default=False,)
    created_at = models.DateTimeField(
        auto_now_add=True)
    updated_at = models.DateTimeField(
        auto_now_add=True)


class HomePageWords(models.Model):
    logo = models.CharField(max_length=254)
    title = models.CharField(max_length=254)
    subtitle = models.CharField(max_length=254)


class Contact(models.Model):
    contact_name = models.CharField(max_length=60)
    email = models.EmailField(max_length=100)
    subject = models.CharField(max_length=60)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, )
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'contact'
        verbose_name_plural = 'contacts'

    def __str__(self):
        return self.contact_name


class NewsletterSubscription(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email


class Features(models.Model):
    featureName = models.CharField(max_length=254)
    featureIcon = models.CharField(max_length=254)
