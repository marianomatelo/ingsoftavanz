# Generated by Django 2.2.6 on 2019-11-01 14:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pg', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='rol',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
    ]
