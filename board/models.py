from django.db import models

class Posts(models.Model):
    author = models.CharField(max_length=-1)
    title = models.CharField(max_length=-1)
    content = models.CharField(max_length=-1)
    created_at = models.DateTimeField()
    updated_at = models.CharField(max_length=-1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'posts'
        app_label = 'postgresql'
