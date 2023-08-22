from django.db import models
from django.urls import reverse
from review.models import Review
from django.db.models.enums import Choices
import uuid

# Create your models here.
# class Profiles(models.Model):
#     first_name   = models.CharField(max_length=120)
#     last_name    = models.CharField(max_length=120, blank=True, null=True)
#     email        = models.EmailField()
#     phone_number = models.CharField(max_length=12)
#     address      = models.TextField(max_length=120)
#     postal_code  = models.CharField(max_length=10)

#     def get_absolute_url(self):
#         return reverse("profiles:profile-detail", kwargs={"id": self.id})


# Drop down
PROVINCES = (
    ('GP','GAUTENG'),
    ('EC', 'EASTERN CAPE'),
    ('WC','WESTERN CAPE'),
    ('NC','NORTHERN CAPE'),
    ('L','LIMPOPO'),
    ('MP','MPUMALANGA'),
    ('NW','NORTH WEST'),
    ('KZ','KWAZULU NATAL'),
    ('FS','FREE STATE')
)
MUNICIPALITIES =(
    # Gauteng
    ('City of Ekurhuleni Metropolitan', 'Ekurhuleni'),
    ('City of Johannesburg Metropolitan','Johannesburg'),
    ('City of Tshwane Metropolitan','Tshwane'),
    ('Sedibeng District','Sedibeng'),
    ('Emfuleni Local','Emfuleni'),
    ('Lesedi Local','Lesedi'),
    ('Midvaal Local','Midvaal'),
    ('West Rand District','West Rand'),
    ('Merafong City Local','Merafong'),
    ('Mogale City Local','Mogale'),
    ('Rand West City Local','Rand West City')
)
ETYPE =(
    ('Hospital','HOSPITAL'),
    ('School','SCHOOL'),
    ('Clinic','CLINIC'),
    ('Police Station','POLICE STATION'),
    ('Municipal Office','MUNICIPAL OFFICE'),
    ('Utility','UTILITY'),
)

class Entity(models.Model):
    id = models.IntegerField(primary_key=True, default=uuid.uuid4)
    entity_name = models.CharField(max_length=200)
    type = models.TextField(blank=True, choices=ETYPE)
    description = models.TextField(blank=True)
    services = models.TextField(blank=True)

    address = models.CharField(max_length=300)
    area = models.CharField(max_length=200, blank=True)
    town = models.CharField(max_length=120)
    gps_coordinates = models.CharField(max_length=40, blank=True, null=True)
    lon = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    lat = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    postal_add = models.CharField(max_length=200, blank=True)
    postal_code = models.CharField(max_length=8, blank=True)
    contact_no = models.CharField(max_length=20)
    contact_no2 = models.CharField(("contact 2"), max_length=20, blank=True)
    email = models.EmailField(max_length=200, blank=True)

    location = models.CharField(max_length=120, blank=True, null=True)
    
    municipality =models.CharField(max_length=200)
    province = models.CharField(max_length=20, choices=PROVINCES, default='GP')

    sector = models.CharField(max_length=200, null=True, blank=True)
    department = models.CharField(max_length=200, blank=True)
    profileimg = models.ImageField(upload_to='profile_images', default = 'blank-profile-picture.png', null=True, blank=True)
    
    website = models.URLField(max_length=200, blank=True)
    reviews = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='entity_reviews', null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    # def _str_(self):
    #     return self.entity_name
    def get_absolute_url(self):
        return reverse("profiles:entity-detail", kwargs={"id": self.id})