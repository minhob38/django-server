from rest_framework import serializers
from .models import SeoulSggs


class SeoulSggsSerializer(serializers.ModelSerializer):
    geom_text = serializers.CharField()
    center_point = serializers.CharField()

    class Meta:
        model = SeoulSggs
        # fields = "__all__"
        fields = (
            "gid",
            "adm_sect_c",
            "sgg_nm",
            "sgg_oid",
            "col_adm_se",
            "geom_text",
            "center_point",
        )
