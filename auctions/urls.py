from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing", views.create_listing, name="create_listing"),
    path("listing_page/<int:listing_id>",views.listing_page, name="listing_page"),
    path("addwatch_list/<int:listing_id>", views.add_watchlist, name="add_watchlist"),
    path("removewatch_list/<int:listing_id>", views.remove_watchlist, name="remove_watchlist"),
    path("close_auction/<int:listing_id>", views.close_auction, name="close_auction"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("categories", views.categories, name="categories"),
    path("category/<str:category>", views.category, name="category"),
    path("add_comment/<int:listing_id>", views.add_comment, name="add_comment"),
]
