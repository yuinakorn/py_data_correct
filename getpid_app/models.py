from django.db import models

# Create your models here.
# from django.contrib.auth.models import AbstractUser
#
#
# class CustomUser(AbstractUser):
#     id = models.IntegerField(primary_key=True)
#     firstname = models.CharField(max_length=50)
#     lastname = models.CharField(max_length=50)
#     email = models.EmailField(max_length=150)
#     officename = models.CharField(max_length=200)
#     username = models.CharField(unique=True, max_length=50)
#     password = models.CharField(max_length=50)
#     lastlogin = models.CharField(max_length=50)
#     status = models.CharField(max_length=50)
#     cid = models.CharField(max_length=13)
#     mobile = models.CharField(max_length=20)
#     off_name = models.CharField(max_length=200)
#
#     class Meta:
#         db_table = 'sys_member'
#         unique_together = ('username',)
