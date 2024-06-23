from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.



class CustomUser(AbstractUser):
   USER_TYPE_CHOICES =(
      ('ops','ops User'),
      ('client','client User')
   )
   user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)


class UploadFile(models.Model):
   type = models.CharField(max_length=30,default="pdf")
   filename = models.CharField(max_length=50,primary_key=True)
   upload_at = models.DateTimeField(auto_now_add = True)

   class Meta:
       unique_together = ('filename','type')