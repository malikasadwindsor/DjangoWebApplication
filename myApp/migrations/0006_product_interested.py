# Generated by Django 3.2.15 on 2022-11-16 02:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myApp', '0005_alter_order_orderstatus'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='interested',
            field=models.PositiveIntegerField(choices=[(1, 'Yes'), (0, 'No')], default=0),
        ),
    ]