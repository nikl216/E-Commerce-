# Generated by Django 3.1.1 on 2020-09-27 16:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0007_auctionlisting_listed_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='bid',
            name='number',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
