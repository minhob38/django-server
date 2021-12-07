from rest_framework import serializers
from .models import SeoulSgg

class SeoulSggSerializer(serializers.ModelSerializer) :
    geom_text = serializers.CharField()

    class Meta:
        model = SeoulSgg
        # fields = "__all__"
        fields = ("gid", "adm_sect_c", "sgg_nm", "sgg_oid", "col_adm_se", "geom_text")
