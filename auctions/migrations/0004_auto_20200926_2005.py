# Generated by Django 3.1.1 on 2020-09-26 14:35

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_auto_20200926_1650'),
    ]

    operations = [
        migrations.AddField(
            model_name='auctionlisting',
            name='category',
            field=models.CharField(blank=True, max_length=12),
        ),
        migrations.AddField(
            model_name='auctionlisting',
            name='description',
            field=models.CharField(default=django.utils.timezone.now, max_length=50),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='auctionlisting',
            name='image_url',
            field=models.URLField(blank=True),
        ),
    ]
