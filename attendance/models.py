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


    def __str__(self):
        return self.name

class Attendance(models.Model):
    date = models.DateField()
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE)
    is_present = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.farmer.name} - {self.date} - {'Present' if self.is_present else 'Absent'}"


    class Meta:
        db_table = 'attendance'
        ordering = ['-date']
