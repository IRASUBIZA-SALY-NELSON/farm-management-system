from django.db import models

# Create your models here.

class Farmer(models.Model):
    name = models.CharField(max_length=100)
    farm = models.CharField(max_length=100)
    age = models.IntegerField()
    location = models.CharField(max_length=100)

    class Meta:
        db_table = 'farmer'
        ordering = ['name']


class Attendance(models.Model):
    date = models.DateField()
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE)
    is_present = models.BooleanField(default=False)


    class Meta:
        db_table = 'attendance'
        ordering = ['-date']


