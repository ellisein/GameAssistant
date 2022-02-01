from django.db import models


class WowItemMedia(models.Model):
	item_id = models.IntegerField(primary_key=True)
	media_url = models.CharField(max_length=128)

class WowSpellMedia(models.Model):
	spell_id = models.IntegerField(primary_key=True)
	media_url = models.CharField(max_length=128)

class WowAffixMedia(models.Model):
	affix_id = models.IntegerField(primary_key=True)
	media_url = models.CharField(max_length=128)

class Minecraft3dTexture(models.Model):
	name = models.CharField(max_length=32, primary_key=True)
	skin = models.ImageField(upload_to='mc_skin')
	url = models.TextField(null=True)
