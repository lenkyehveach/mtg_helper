from django.db import models

# Create your models here.

class Neo(models.Model):
    name = models.CharField(max_length=54, blank=True, null=True)
    colors = models.CharField(max_length=50, blank=True, null=True)
    coloridentity = models.CharField(db_column='colorIdentity', max_length=50, blank=True, null=True)  # Field name made lowercase.
    manacost = models.CharField(db_column='manaCost', max_length=50, blank=True, null=True)  # Field name made lowercase.
    manavalue = models.PositiveIntegerField(db_column='manaValue', blank=True, null=True)  # Field name made lowercase.
    originaltype = models.CharField(db_column='originalType', max_length=50, blank=True, null=True)  # Field name made lowercase.
    types = models.CharField(max_length=50, blank=True, null=True)
    subtypes = models.CharField(max_length=50, blank=True, null=True)
    supertypes = models.CharField(max_length=50, blank=True, null=True)
    originaltext = models.TextField(db_column='originalText', blank=True, null=True)  # Field name made lowercase.
    keywords = models.CharField(max_length=50, blank=True, null=True)
    power = models.PositiveIntegerField(blank=True, null=True)
    toughness = models.PositiveIntegerField(blank=True, null=True)
    rarity = models.CharField(max_length=10, blank=True, null=True)
    setcode = models.CharField(db_column='setCode', max_length=3, blank=True, null=True)  # Field name made lowercase.
    image_ref = models.CharField(max_length=50, blank=True, null=True)
    cardid = models.AutoField(db_column='cardID', primary_key=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'neo'
