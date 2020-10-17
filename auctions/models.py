from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class AuctionListing(models.Model):
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=50)
    image_url = models.URLField(blank=True)
    price = models.DecimalField(max_digits=4,decimal_places=2)
    created_date = models.DateTimeField()
    listed_by= models.IntegerField()
    category = models.CharField(max_length=12,blank=True)
    winner_id = models.IntegerField(blank=True,null=True)
    closed = models.BooleanField(default=False)


    def __str__(self):
        return f"{self.pk}: {self.title}"

class Bid(models.Model):
    auction = models.IntegerField()
    bid = models.DecimalField(max_digits=4,decimal_places=2)
    user= models.IntegerField()

    def __str__(self):
        return f"{self.pk}: {self.auction} , {self.bid}"

class Comment(models.Model):
    auction = models.IntegerField()
    user = user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="comments")
    comment = models.CharField(max_length=55)
    def __str__(self):
     return f"{self.pk}: {self.auction} , {self.comment}"

class Watchlist(models.Model):
    user_id= models.IntegerField()
    auction_id=models.IntegerField()