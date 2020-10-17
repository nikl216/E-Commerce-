from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from .models import AuctionListing,Bid,Comment,Watchlist
from datetime import datetime
from django.db.models import Max
from django.contrib.auth.decorators import login_required
from .models import User

class create_listing_form(forms.Form):
    title = forms.CharField(label="title",max_length=30,widget=forms.TextInput(attrs={"class":"col-6 form-control","AutoComplete":"off"}))
    description = forms.CharField(label="description",max_length=50,widget=forms.TextInput(attrs={"class":"col-6 form-control","AutoComplete":"off"}))
    price = forms.DecimalField(label="price",max_digits=4,decimal_places=2,widget=forms.TextInput(attrs={"class":" col-6 form-control","AutoComplete":"off"}))
    imageurl=forms.URLField(label="imageurl",required=False,widget=forms.TextInput(attrs={"class":"col-6 form-control","AutoComplete":"off"}))
    category = forms.CharField(label="category",required=False,widget=forms.TextInput(attrs={"class":"col-6 form-control","AutoComplete":"off"}))

class bid_form(forms.Form):
    bid = forms.DecimalField(label="",max_digits=4,decimal_places=2,widget=forms.TextInput(attrs={"placeholder":"Bid","class":" col-6 form-control","AutoComplete":"off"}))

def index(request):
    listings=AuctionListing.objects.all()
    
    return render(request, "auctions/index.html",{
        "listings":listings
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")

@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        register="auctions/register.html"
        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, register, {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, register, {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

@login_required    
def create_listing(request):
    if request.method == "POST":
        form=create_listing_form(request.POST)
        if form.is_valid():
            title= form.cleaned_data["title"]
            description= form.cleaned_data["description"]
            category= form.cleaned_data["category"]
            imageurl= form.cleaned_data["imageurl"]
            price= form.cleaned_data["price"]
            listing=AuctionListing.objects.create(title=title,description=description,price=price,category=category,
            image_url=imageurl,created_date=datetime.now(),listed_by=request.user.pk)
            return HttpResponseRedirect(reverse("index"))

        else:
            return render(request, "auctions/create_listing.html",{
            "form":form
        })

        
    else:
        return render(request, "auctions/create_listing.html",{
            "form":create_listing_form
        })


def listing_page(request,listing_id):
    listing=AuctionListing.objects.get(pk=listing_id)
    created_by= User.objects.get(pk=listing.listed_by)
    iswinner=False
    current_user_id=request.user.id
    if listing.closed:
        if listing.winner_id==current_user_id:
            iswinner=True
    if created_by.pk==request.user.pk:
        isowner=True
    else:
        isowner=False
    try:
        bids=Bid.objects.filter(auction=listing_id)
    except Bid.DoesNotExist:
        bids=None
    bidform=bid_form()
    
    if(bids):
        bidcount=bids.count()
        price=Bid.objects.filter(auction=listing_id).aggregate(Max('bid'))['bid__max']
       
    else:
        bidcount=0
        price=listing.price   

    watchlist=Watchlist.objects.filter(user_id=current_user_id,auction_id=listing_id)
    if not watchlist:
        iswatchlisted=False
    else:
        iswatchlisted=True
    comments=Comment.objects.filter(auction=listing_id)
    if request.method == "GET":
        return render(request,"auctions/listingpage.html",{"listing":listing,"created_by":created_by,"form":bidform,"bid":price,"bidcount":bidcount,"isowner":isowner,"closed":listing.closed,"iswinner":iswinner,"iswatchlisted":iswatchlisted,"comments":comments})

    else:
        if request.user.is_authenticated:
            form=bid_form(request.POST)
            if form.is_valid():
                bid=form.cleaned_data["bid"]
                if bid <= price:
                    return render(request,"auctions/listingpage.html",{"listing":listing,"created_by":created_by,"form":bidform,"bid":price,"bidcount":bidcount,"message":"Bid must be greater than the current price","isowner":isowner,"closed":listing.closed,"iswinnner":iswinner,"iswatchlisted":iswatchlisted,"comments":comments})
                else:
                    addbid=Bid.objects.create(user=request.user.pk,auction=listing_id,bid=bid)
                    return HttpResponseRedirect(reverse("listing_page" , kwargs={'listing_id':listing_id}))
            else:
                render(request,"auctions/listingpage.html",{"listing":listing,"created_by":created_by,"form":form,"bid":price,"bidcount":bidcount,"isowner":isowner,"closed":listing.closed,"iswinnner":iswinner,"iswatchlisted":iswatchlisted,"comments":comments})
        else:
            return render(request, "auctions/apology.html",{"message":"Please log in to view listing"})

@login_required
def add_watchlist(request,listing_id):
    watchlist =Watchlist.objects.create(user_id=request.user.pk,auction_id=listing_id)
    
    return HttpResponseRedirect(reverse('listing_page', kwargs={'listing_id':listing_id}))

def remove_watchlist(request,listing_id):
    watchlist =Watchlist.objects.filter(user_id=request.user.pk,auction_id=listing_id).delete()
    return HttpResponseRedirect(reverse('listing_page', kwargs={'listing_id':listing_id}))

@login_required
def close_auction(request,listing_id):
    winning_bid=Bid.objects.filter(auction=listing_id).order_by('-bid').first()
    listing=AuctionListing.objects.get(pk=listing_id)
    listing.winner_id=winning_bid.user

    listing.closed=True
    listing.save()
    return HttpResponseRedirect(reverse('index'))

@login_required
def watchlist(request):
    watchlists=Watchlist.objects.filter(user_id=request.user.pk)
    watchlists_ids=set()
    for watchlist in watchlists:
        watchlists_ids.add(watchlist.auction_id)

    listings=AuctionListing.objects.filter(pk__in=watchlists_ids)
    
    return render(request, "auctions/auctionlayout.html",{
        "listings":listings,
        "title":"Watchlist"
    })
    

def add_comment(request,listing_id):
    if request.method == "POST":
        if request.user.is_authenticated:
            comment=request.POST['comment']
            create_comment=Comment.objects.create(auction=listing_id,user=request.user,comment=comment)
            return HttpResponseRedirect(reverse('listing_page', kwargs={'listing_id':listing_id}))
        else:
            return render(request, "auctions/apology.html",{"message":"Please log in to view listing"})
@login_required
def categories(request):
    listings=AuctionListing.objects.exclude(category="")
    categories=set()
    for a in listings:
        categories.add(a.category)
    return render(request,"auctions/categories.html",{"categories":categories})

@login_required
def category(request, category):
    listings =AuctionListing.objects.filter(category=category)
    return render(request, "auctions/auctionlayout.html",{
        "listings":listings,
        "title":category
    })
