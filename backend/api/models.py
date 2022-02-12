from django.db import models


class Country(models.Model):
    name = models.CharField(max_length=60)
    image = models.ImageField(null=True, blank=True, upload_to="static/")
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name
