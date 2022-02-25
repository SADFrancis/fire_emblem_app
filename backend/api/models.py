from django.db import models


# class Country(models.Model):
#     name = models.CharField(max_length=60)
#     image = models.ImageField(null=True, blank=True, upload_to="static/")
#     description = models.TextField(null=True, blank=True)

    # def __str__(self):
    #     return self.name

class Character(models.Model):
    name = models.CharField(max_length=60)
    title = models.CharField(max_length=100)
    game_origin = models.CharField(null=True, blank=True, max_length=100)
    ref_id = models.CharField(null=True, max_length=20)
    ref_link = models.CharField(null=True, max_length=100)
    icon_link = models.CharField(null=True, max_length=100)
    sprite= models.CharField(null=True, max_length=100)
    portrait= models.CharField(null=True, max_length=100)
    attack= models.CharField(null=True, max_length=100)
    special= models.CharField(null=True, max_length=100)
    damaged= models.CharField(null=True, max_length=100)
    voice_1 = models.CharField(null=True, max_length=100)
    voice_2 = models.CharField(null=True, max_length=100)
    line_1 = models.TextField(null=True)
    line_2 = models.TextField(null=True)
    summary = models.TextField(null=True)
    realm = models.CharField(max_length=60)
    release_date = models.DateTimeField(auto_now=False)
    index = models.IntegerField()

    def __str__(self):
        return self.name + " " + self.title