# Generated by Django 4.2.10 on 2024-03-01 14:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0006_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='is_reply',
            field=models.BooleanField(default=False),
        ),
    ]
