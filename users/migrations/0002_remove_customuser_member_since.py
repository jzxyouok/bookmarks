# Generated by Django 2.1.4 on 2018-12-31 07:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='member_since',
        ),
    ]
