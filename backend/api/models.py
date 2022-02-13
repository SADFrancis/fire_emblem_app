from django.db import models


class Country(models.Model):
    name = models.CharField(max_length=60)
    image = models.ImageField(null=True, blank=True, upload_to="static/")
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

class Character(models.Model):
    name = models.CharField(max_length=60)
    title = models.CharField(max_length=100)
    ref_link = models.CharField(null=True, max_length=100)
    icon_link = models.CharField(null=True, max_length=100)
    miniImageLink= models.CharField(null=True, max_length=100)
    imageLink = models.CharField(null=True, max_length=260)
    voice_1 = models.CharField(null=True, max_length=100)
    voice_2 = models.CharField(null=True, max_length=100)
    summary = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name + " " + self.title