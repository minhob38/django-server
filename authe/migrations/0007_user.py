# Generated by Django 3.2.9 on 2021-12-05 15:33

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('authe', '0006_delete_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('email', models.TextField(unique=True)),
                ('password', models.TextField()),
                ('created_at', models.DateTimeField()),
            ],
            options={
                'db_table': 'authe_user',
                'managed': False,
            },
        ),
    ]
