# Generated by Django 5.0.6 on 2024-06-12 10:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('themes', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='layergroupmp',
            name='name',
            field=models.CharField(max_length=128),
        ),
    ]