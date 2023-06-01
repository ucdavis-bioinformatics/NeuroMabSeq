from rest_framework import serializers
from .models import *

# can also use a Model Serializer here
class TrimmerEntrySerializer(serializers.ModelSerializer):

    class Meta:
        model = TrimmerEntry
        fields = ['id', 'mabid', 'show_on_web', 'category', 'protein_target', 'heavy_count', 'light_count', 'get_category',
                  'get_protein_target', 'get_url', 'clonality', 'max_lcstars', 'max_hcstars', 'maxavgstars']


# can also use a Model Serializer here
class TrimmerStatusSerializer(serializers.ModelSerializer):
    entry = serializers.StringRelatedField(many=False)
    class Meta:
        model = TrimmerEntryStatus
        fields = ['id', 'sample_name', 'plate_location', 'volume', 'concentration', 'comments', 'failure',
                  'amplicon_concentration', 'inline_index', 'inline_index_name', 'LCs_reported', 'HCs_reported',
                  'entry']
