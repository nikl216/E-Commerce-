# Generated by Django 3.1.1 on 2020-09-27 16:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0008_bid_number'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bid',
            old_name='number',
            new_name='user',
        ),
    ]
