from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy

from . import util

from .models import User, Listing, Bid
from .forms import ListingForm, BidForm
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

    def get_queryset(self):
        return Listing.objects.filter(active=True)


class ListingDetailView(DetailView):
    model = Listing
    # template_name = 'auctions/itemdetail.html'
    context_object_name = "listing"

    def get_context_data(self, **kwargs):
        context = super(ListingDetailView, self).get_context_data(**kwargs)
        # Suplement Listing Details  with Bid Details
        context['bid_details'] = util.get_bid_details(self.kwargs['pk'])
        return context


class ListingCreateView(LoginRequiredMixin, CreateView):
    model = Listing
    form_class = ListingForm
    '''  
    template_name = listing_form.html
    This is the default name for the template to render the Listing Create form
    and hence does not have to be explicitly identified
    '''
    success_url = reverse_lazy('index')

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
    # TODO - Attempt to improve the code above
    # TODO Add confirmation before the listing is closed

    except ObjectDoesNotExist:
        raise Http404("Listing does not exist")

    return HttpResponseRedirect(reverse("index"))


class BidCreateView(LoginRequiredMixin, CreateView):
    model = Bid
    form_class = BidForm
    #   Using default template 'bid_form.html'. Explicit declaration not required

    success_url = reverse_lazy('index')

    login_url = 'login'
    '''
    Unauthenticated users will be automatically directed to the 'login' page
    '''

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
