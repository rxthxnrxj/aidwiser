from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Driver(models.Model):
    STATUS = (
        ('Available', 'Available'),
        ('Busy', 'Busy')
    )
    amb_assgn = models.BooleanField(default=False, null=True, blank=False)
    aid_assgn = models.BooleanField(default=False, null=True, blank=False)
    name = models.CharField(max_length=100, null=True)
    phone = models.IntegerField(null=True, blank=True)
    performance = models.FloatField(default=0, null=True, blank=True)
    status = models.CharField(max_length=200, null=True, choices=STATUS)

    def __str__(self):
        return str(self.name)


class Hospital(models.Model):
    STATUS = (
        ('Available', 'Available'),
        ('Not Available', 'Not Available'),
    )
    name = models.CharField(max_length=100, null=True)
    emergency = models.BooleanField(default=False, null=True, blank=False)
    latitude = models.FloatField(default=0, null=True, blank=True)
    longitude = models.FloatField(default=0, null=True, blank=True)
    doc = models.BooleanField(default=False, null=True, blank=False)
    status = models.CharField(max_length=200, null=True, choices=STATUS)

    def __str__(self):
        return str(self.name)


class Aid(models.Model):
    STATUS = (
        ('Ambulance Not assigned', 'Ambulance Not assigned'),
        ('Ambulance Assigned', 'Ambulance Assigned'),
        ('Ambulance Not Available', 'Ambulance Not Available'),
        ('Ambulance arrivingg', 'Ambulance arrivingg'),
    )
    aid = models.OneToOneField(
        User, on_delete=models.CASCADE, null=True, blank=True)
    latitude = models.FloatField(default=0, null=True, blank=True)
    longitude = models.FloatField(default=0, null=True, blank=True)
    time = models.DateTimeField(auto_now_add=True)
    aid_details = models.CharField(max_length=200, null=True)
    status = models.CharField(max_length=200, null=True, choices=STATUS)

    def __str__(self):
        return str(self.latitude)


class Ambulance(models.Model):
    STATUS = (
        ('Available', 'Available'),
        ('Aid Assigned', 'Aid Assigned'),
    )
    regno = models.CharField(max_length=10, null=True)
    drivername=models.CharField(max_length=100, null=True)
    contact=models.IntegerField(null=True, blank=True)
    latitude = models.FloatField(default=0, null=True, blank=True)
    longitude = models.FloatField(default=0, null=True, blank=True)
    ais = models.BooleanField(default=False, null=True, blank=False)
    bis = models.BooleanField(default=False, null=True, blank=False)
    status = models.CharField(max_length=200, null=True, choices=STATUS)
    hosp_assgn = models.BooleanField(default=False, null=True, blank=False)
    aid = models.ForeignKey(
        Aid, on_delete=models.CASCADE, blank=True, null=True)
    hospital = models.ForeignKey(
        Hospital, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return str(self.regno)


class Doctor(models.Model):
    STATUS = (
        ('Available', 'Available'),
        ('Busy', 'Busy'),
        ('Contact', 'Contact')
    )
    name = models.CharField(max_length=100, null=True)
    hospital = models.ForeignKey(
        Hospital, on_delete=models.CASCADE, blank=True, null=True)
    assgn = models.OneToOneField(
        Aid, on_delete=models.CASCADE, blank=True, null=True)
    spl = models.CharField(max_length=100, null=True)
    status = models.CharField(max_length=200, null=True, choices=STATUS)
    performance = models.FloatField(default=0, null=True, blank=True)

    def __str__(self):
        return str(self.name)
