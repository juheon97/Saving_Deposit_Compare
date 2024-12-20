# Generated by Django 4.2.4 on 2024-11-25 17:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='balance_deposit',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name='user',
            name='balance_saving',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=7),
        ),
    ]
