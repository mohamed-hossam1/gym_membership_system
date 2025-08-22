from django.contrib.auth.models import User
from django.db import models


class Member(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='member_profile')
    name = models.CharField(max_length=100)
    user_name = models.CharField(max_length=50, unique=True)
    age = models.IntegerField()
    phone = models.CharField(max_length=15, unique=True)
    subscription_start_date = models.DateField()
    subscription_end_date = models.DateField()
    image = models.ImageField(upload_to='members_images/', default='members_images/Unknown.png')
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True, null=True)
    unique_id = models.CharField(max_length=100,unique=True)

    def __str__(self):
        return str(self.name)