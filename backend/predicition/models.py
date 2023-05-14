from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin,UserManager
# Create your models here.
class ProjectMedia(models.Model):
    tag = models.CharField(max_length=300, null=False, blank=False)
    image = models.ImageField(upload_to="projectmedia", null=False, blank=False)
    def __str__(self):
        return self.tag
    
class Predictions(models.Model):
    image = models.ImageField(upload_to="projectmedia", null=False, blank=False)
    output = models.CharField(max_length=300, null=True, blank=True)
    predicted_on = models.DateTimeField(auto_now=True,null=True)

class User(AbstractBaseUser):
    name = models.CharField(max_length=30,null=False,blank=False)
    email = models.EmailField(max_length=255,unique=True)
    username = models.CharField(max_length=100, null=True, blank=True)
    history = models.ManyToManyField(Predictions,blank=True)

    objects = UserManager()
    USERNAME_FIELD = "email"

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.pk:
            super().save(*args, **kwargs)
            self.history.clear()  # Clear the default history value after saving
        else:
            super().save(*args, **kwargs)

class Refrences(models.Model):
    ref = models.CharField(max_length=1000,null=False,blank=False)
    disease_name = models.CharField(max_length=100,null=False,blank=False)
    def __str__(self):
        return self.disease_name

class PrecautionTable(models.Model):
    cure_text = models.CharField(max_length=2000,blank=False,null=False)
    refrences = models.ManyToManyField(Refrences,blank=False)
    def __str__(self):
        return str(self.id)