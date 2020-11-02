import re
from .models import Listing, Bid, Comment
from django.db.models import Max


def get_bid_details(id):
    """
    Returns the 'bid_count' and 'max_bid' associated with a Listing
    """
    filtered_bids = Bid.objects.filter(title_id=id).exclude(active=False)
    bid_count = filtered_bids.count()
    max_bid = filtered_bids.aggregate(Max('bid_amount'))['bid_amount__max']

    bid_details = {"bid_count": bid_count,
                   "max_bid": max_bid,
                   }
    return bid_details


def get_listing_details(id):
    """
    Returns the fields for the Listing model for reference in templates
    """
    title = Listing.objects.get(pk=id).title
    starting_bid = Listing.objects.get(pk=id).starting_bid
    image = Listing.objects.get(pk=id).image

    listing_details = {"title": title,
                       "starting_bid": starting_bid,
                       "image": image,
                       }
    return listing_details


def get_comments(id):
    comments = Comment.objects.filter(title_id=id)
    return comments


def get_my_bid(t_id, u_id):
        my_bid = Bid.objects.filter(title_id=t_id, user_id=u_id)
        if my_bid:
            return my_bid[0]