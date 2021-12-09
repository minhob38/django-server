from django.db import models

class Posts(models.Model):
    """
    - inspect해도 postgresql의 table config와 같지 않으므로 다소 수정이 필요
    - max_length 없으면, serializer.is_valid()에서 에러 발생
    """
    author = models.CharField(max_length=10)
    title = models.CharField(max_length=50)
    content = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(blank=True, null=True, auto_now=True)

    class Meta:
        managed = False
        db_table = 'posts'
        app_label = 'postgresql'
