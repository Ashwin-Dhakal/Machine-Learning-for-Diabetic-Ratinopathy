from django.db import models


class All_hostel(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200,default='')
    location = models.CharField(max_length=200,default='')
    address = models.CharField(max_length=200,default='')
    gender = models.CharField(max_length=20,default='')
    phone_number = models.CharField(max_length=200,default='')
    facilities = models.CharField(max_length=500, default='DEFAULT VALUE')
    admission_fee = models.CharField(max_length=200,default='')
    monthly_charge = models.CharField(max_length=200,default='')
    owner = models.CharField(max_length=100,default='')
    email = models.EmailField(max_length=100,default='')
    deposit = models.CharField(max_length=100,default='')
    latitude = models.CharField(max_length=200,default='')
    longitude = models.CharField(max_length=200,default='')
    image = models.FileField(null=True, blank=True)
    image2 =models.FileField(null=True, blank=True)

    # location_name = models.ForeignKey(location_name, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name
