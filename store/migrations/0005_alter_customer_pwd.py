# Generated by Django 3.2.5 on 2021-11-26 08:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_customer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='pwd',
            field=models.CharField(max_length=200),
        ),
    ]
