from django.db import models


class SeoulSggs(models.Model):
    gid = models.AutoField(primary_key=True)
    adm_sect_c = models.CharField(max_length=254, blank=True, null=True)
    sgg_nm = models.CharField(max_length=254, blank=True, null=True)
    sgg_oid = models.IntegerField(blank=True, null=True)
    col_adm_se = models.CharField(max_length=254, blank=True, null=True)
    field_gid = models.IntegerField(db_column="__gid", blank=True, null=True)
    geom = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "seoul_sggs"
        app_label = "postgresql"
