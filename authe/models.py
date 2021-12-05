from django.db import models

class User(models.Model):
    id = models.AutoField(primary_key = True)
    email = models.TextField(unique = True)
    password = models.TextField()
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        app_label = "postgresql"
        db_table = 'authe_user'

    def __str__(self):
        return f'type:{type(self)}) id:{self.id} email:{self.email} password:{self.password} created_at:{self.created_at}'
