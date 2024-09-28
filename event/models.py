from django.db import models

class Event(models.Model):
    name = models.CharField(max_length=40)
    description = models.TextField()
    day_month_year = models.DateField()
    time = models.TimeField()
    #group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="group") №нужно будет прикреплять евенты к группам, когда они появятся
    
