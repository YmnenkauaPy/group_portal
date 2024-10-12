from django.db import models
from group.models import Group
from django.conf import settings

class Material(models.Model):
    name = models.CharField(max_length=32)
    content = models.FileField(upload_to = "materials_media/", blank=True, null=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='author_of_material')
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="materials_group")
    