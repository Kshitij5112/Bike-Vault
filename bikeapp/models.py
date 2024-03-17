from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Bike(models.Model):
    brand=models.CharField(max_length=20)
    name=models.CharField(max_length=20)
    type=models.CharField(max_length=20)
    price=models.IntegerField()
    details=models.CharField(max_length=500,default="")
    year=models.DateField()
    pimage = models.ImageField(upload_to='image', default = 1)

class Cart(models.Model):
    # foreign key must be set as a reference to the object 
    pid = models.ForeignKey(Bike,on_delete = models.CASCADE, db_column='pid')
    uid = models.ForeignKey(User,on_delete = models.CASCADE, db_column='uid')
    quantity = models.IntegerField(default = 1)

class Order(models.Model):
    orderid=models.IntegerField()
    uid=models.ForeignKey(User,on_delete=models.CASCADE, db_column="uid")
    pid=models.ForeignKey(Bike,on_delete=models.CASCADE, db_column="pid")
    quantity=models.IntegerField()