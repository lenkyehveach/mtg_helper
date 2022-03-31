from rest_framework import serializers
from .models import Neo

class NeoSerializer(serializers.ModelSerializer):
  class Meta: 
    model = Neo 
    fields = (
      "name", "colors", "coloridentity", "manacost", "manavalue", "originaltype", "types", "subtypes", "supertypes", "originaltext", "keywords", "power", "toughness", "rarity", "setcode", "image_ref", "cardid"

    )

 