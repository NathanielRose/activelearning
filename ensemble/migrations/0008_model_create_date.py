# Generated by Django 2.1.2 on 2018-12-06 23:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ensemble', '0007_auto_20181206_2041'),
    ]

    operations = [
        migrations.AddField(
            model_name='model',
            name='create_date',
            field=models.TextField(null=True),
        ),
    ]