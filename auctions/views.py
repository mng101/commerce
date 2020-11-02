from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy

from . import util

from .models import User, Listing, Bid, Comment, Watchlist
from .forms import ListingForm, BidForm, CommentForm, WatchlistForm
from django.db.models import Max

from django.views.generic import (View, TemplateView, ListView,
                                  DetailView, CreateView, DeleteView,
                                  UpdateView, )

'''
View in distribution code replace with a ListingListView
'''


# def index(request):
#     return render(request, "auctions/index.html")


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


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


'''
Start of updates to the distribution code
'''


class ListingListView(ListView):
    template_name = 'auctions/index.html'
    context_object_name = 'listing_list'

    def get_queryset(self, **kwargs):
        queryset = Listing.objects.filter(active=True)

        if self.request.GET.get('user'):
            queryset = queryset.filter(user_id__username=self.request.GET.get('user'))
        elif self.request.GET.get('category'):
            queryset = queryset.filter(category=self.request.GET.get('category'))

        return queryset

    def get_context_data(self, **kwargs):
        context = super(ListingListView, self).get_context_data(**kwargs)
        if self.request.GET.get('user'):
            context['PageTitle'] = 'Listing for User: ' + self.request.GET.get('user')
        elif self.request.GET.get('category'):
            context['PageTitle'] = 'Listing for category: ' + (self.request.GET.get('category'))

        return context


class ListingDetailView(DetailView):
    model = Listing
    context_object_name = "listing"

    def get_context_data(self, **kwargs):
        context = super(ListingDetailView, self).get_context_data(**kwargs)
        # Suplement Listing Details  with Comments posted
        context['comments'] = util.get_comments(self.kwargs['pk'])
        if self.request.user.id is not None:
            # If the user is authenticated, get additional info for the listing details page
            if Watchlist.objects.filter(title_id=self.kwargs['pk'], user_id=self.request.user, active=True):
                context['on_watchlist'] = True
            else:
                context['on_watchlist'] = False

            context['my_bid'] = util.get_my_bid(self.kwargs['pk'], self.request.user)

        return context


class ListingCreateView(LoginRequiredMixin, CreateView):
    model = Listing
    form_class = ListingForm
    # template_name = listing_form.html - Using default template for ListingCreateView

    login_url = 'login'
    '''
    The user will be automatically redirected to the Login view if an unautenticated
    user attempts to create a new Listing
    '''

    def form_valid(self, form):
        form.instance.user_id = self.request.user
        form.instance.valid = True
        return super(ListingCreateView, self).form_valid(form)


class ListingUpdateView(UpdateView):
    model = Listing
    form_class = ListingForm


def close(request, **kwargs):
    try:
        l = Listing.objects.get(id=kwargs['pk'])
        l.active = False
        l.save()

    except ObjectDoesNotExist:
        raise Http404("Listing does not exist")

    return HttpResponseRedirect(reverse("index"))


class BidCreateView(LoginRequiredMixin, CreateView):
    model = Bid
    form_class = BidForm

    login_url = 'login'

    def get_initial(self):
        return {'title_id': self.kwargs['pk'],
                'user_id': self.request.user.id, }

    def get_context_data(self, **kwargs):
        context = super(BidCreateView, self).get_context_data(**kwargs)
        context['listing_details'] = util.get_listing_details(self.kwargs['pk'])
        context['bid_details'] = util.get_bid_details(self.kwargs['pk'])
        return context

    def form_valid(self, form):
        form.instance.user_id = self.request.user
        form.instance.valid = True
        return super(BidCreateView, self).form_valid(form)


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm

    login_url = 'login'

    def get_initial(self):
        return {'title_id': self.kwargs['pk'],
                'user_id': self.request.user.id, }

    def get_context_data(self, **kwargs):
        context = super(CommentCreateView, self).get_context_data(**kwargs)
        context['listing_details'] = util.get_listing_details(self.kwargs['pk'])
        return context

    def form_valid(self, form):
        form.instance.user_id = self.request.user
        form.instance.valid = True
        return super(CommentCreateView, self).form_valid(form)


def add2watchlist(request, **kwargs):
    try:
        w, created = Watchlist.objects.get_or_create(
            title_id=Listing.objects.get(id=kwargs['pk']),
            user_id=request.user,
            active=True,
        )
        print(created)
    except DatabaseError:
        raise Http404("Listing does not exist")

    return HttpResponseRedirect(reverse("index"))


def removewatchlist(request, **kwargs):
    try:
        w = Watchlist.objects.get(title_id=kwargs['pk'], user_id=request.user, active=True)
        w.active = False
        w.save()
    except DatabaseError:
        raise Http404("Watchlist does not exist")

    return HttpResponseRedirect(reverse("index"))


class BidListView(LoginRequiredMixin, ListView):
    Model = Bid
    template_name = 'auctions/bid_list.html'
    contect_object_name = 'listing_list'
    login_url = 'login'

    def get_queryset(self):
        return Bid.objects.filter(user_id__username=self.request.user).distinct().select_related('title_id')

    def get_context_data(self, **kwargs):
        context = super(BidListView, self).get_context_data(**kwargs)
        context['PageTitle'] = 'Items You have Bid On'
        return context


class WatchlistListView(LoginRequiredMixin, ListView):
    Model = Watchlist
    template_name = 'auctions/index.html'
    context_object_name = 'listing_list'
    login_url = 'login'

    def get_queryset(self):
        watchlist_items = Watchlist.objects.filter(user_id__username=self.request.user, active=True).values_list(
            'title_id')
        return Listing.objects.filter(pk__in=watchlist_items)

    def get_context_data(self, **kwargs):
        context = super(WatchlistListView, self).get_context_data(**kwargs)
        context['PageTitle'] = 'Your Watchlist Items'
        return context


class CategoryListView(ListView):
    Model = Listing
    template_name = 'auctions/category_list.html'
    context_object_name = 'category_list'
    login_url = 'login'

    def get_queryset(self):
        queryset = []
        for item in (Listing.objects.filter(active=True).values_list('category').distinct()):
            queryset.append(item[0])
        return queryset
