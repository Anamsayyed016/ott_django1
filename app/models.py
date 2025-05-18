from django.db import models

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    password = models.CharField(max_length=50)
    cpassword = models.CharField(max_length=50)

    def __str__(self):
            return self.username

class Subscription(models.Model):
    plan_name = models.CharField(max_length=100)
    price = models.IntegerField()
    features = models.CharField(max_length=150)
    duration = models.IntegerField()

    def __str__(self):
            return self.plan_name