# Generated by Django 3.1.1 on 2020-09-26 11:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_auctionlistings_bids_comments'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='AuctionListings',
            new_name='AuctionListing',
        ),
        migrations.RenameModel(
            old_name='Bids',
            new_name='Bid',
        ),
        migrations.RenameModel(
            old_name='Comments',
            new_name='Comment',
        ),
    ]
