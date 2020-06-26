from rest_framework import serializers
from .models import *

# can also use a Model Serializer here
class TrimmerEntrySerializer(serializers.ModelSerializer):

    class Meta:
        model = TrimmerEntry
        fields = ['id', 'mabid', 'show_on_web', 'category', 'protein_target', 'heavy_count', 'light_count', 'get_category',
                  'get_protein_target', 'get_url']
