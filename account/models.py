from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    address = models.TextField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    token = models.CharField(max_length=100, blank=True)
    expire = models.DateTimeField(null=True, blank=True)
        
    def __unicode__(self):
        return u'%s' % self.user

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)
