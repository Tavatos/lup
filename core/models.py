import email
from django.db import models
from django.contrib.auth import get_user_model
import uuid
from datetime import datetime
from distutils.command import upload
from pyexpat import model
from statistics import mode


User = get_user_model()

# Create your models here.
# class PublicEntity(models.Model):
    # id = models.IntegerField(primary_key=True)
    # entity_name = models.CharField(max_length=200)
    # description = models.TextField(blank=True)
    # services = models.TextField(blank=True)
    # address = models.CharField(max_length=300)
    # contact_no = models.CharField( max_length=200)
    # contact_no2 = models.CharField((""), max_length=200, blank=True)
    # email_add = models.EmailField(max_length=200)
    # postal_add = models.CharField(max_length=200, blank=True)
    # postal_code = models.IntegerField()
    # sector = models.CharField(max_length=200, null="True", blank=True)
    # department = models.CharField(max_length=200, blank=True)
    # profileimg = models.ImageField(upload_to='profile_images', default = 'blank-profile-picture.png', null="True", blank=True)
    # address = models.CharField(max_length=300)
    # contact_no = models.CharField((""), max_length=200)
    # contact_no2 = models.CharField((""), max_length=200, blank=True)
    # email_add = models.EmailField(max_length=200)
    # postal_add = models.CharField(max_length=200, blank=True)
    # postal_code = models.IntegerField()
    # website = models.URLField((""), max_length=200, blank=True)
    # location = models.CharField(max_length=120, blank=True)
    # municipality =models.CharField(max_length=200)
    # province = models.CharField(max_length=200)
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)


    # def _str_(self):
    #     return self.entity_name

class User_Profile(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    id_user = models.UUIDField(primary_key=True, default=uuid.uuid4)
    email = models.EmailField(blank=True)
    first_name = models.TextField(max_length=20, blank=True)
    last_name = models.TextField(max_length=30, blank=True)
    bio = models.TextField(blank=True)
    profileimg = models.ImageField(upload_to='profile_images', default = 'blank-profile-picture.png')
    location = models.CharField(max_length=120, blank=True)
    address = models.CharField(max_length=120, blank=True)

    def __str__(self):
        return f" Profile for {self.username}"

# class Curator_Profile(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     id_user = models.IntegerField()
#     bio = models.TextField(blank=True)
#     profileimg = models.ImageField(upload_to='profile_images', default = 'blank-profile-picture.png')
#     location = models.CharField(max_length=120, blank=True)

#     def _str_(self):
#         return self.user.username

# class Reveiw(models.Model):
#     id = models.IntegerField(primary_key=True, default=uuid.uuid4)
#     entity = models.TextField(max_length=200)
#     user = models.CharField(max_length=100)
#     created_at = models.DateTimeField(default=datetime.now)
#     no_of_likes = models.IntegerField(default=0)
#     rating = models.IntegerField()
#     comment = models.CharField(max_length=1000, blank=True)
   


# class Forum(models.Model):
#     id = models.IntegerField(primary_key=True, default=uuid.uuid4)
#     user = models.CharField(max_length=100)
#     post = models.TextField(blank=False, max_length=10000)
#     comment = models.TextField(blank=False, max_length=5000)
    
# class Post(models.Model):
#     id = models.IntegerField(primary_key=True, default=uuid.uuid4)
#     user = models.CharField(max_length=100)
#     image = models.ImageField(upload_to='post_images')
#     caption = models.TextField()
#     created_at = models.DateTimeField(default=datetime.now)
#     no_of_likes = models.IntegerField(default=0)

#     def _str_(self):
#         return self.user

