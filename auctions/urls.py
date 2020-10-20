from django.urls import path

from . import views

urlpatterns = [
    #
    # path("", views.Listin, name="index"),
    #
    path("", views.ListingListView.as_view(), name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create/", views.ListingCreateView.as_view(), name="create"),
    path("bid/", views.BidListView.as_view(), name="bid"),
    path('<pk>/', views.ListingDetailView.as_view(), name="detail"),
    path('update/<pk>/', views.ListingUpdateView.as_view(), name="update"),
    path('close/<pk>/', views.close, name="close"),
    path('bid/<pk>/', views.BidCreateView.as_view(), name="bid"),
    path('comment/<pk>/', views.CommentCreateView.as_view(), name="comment"),
    # path('watchlist/<pk>/', views.WatchlistCreateView.as_view(), name="watchlist"),
    path('watchlist/<pk>/', views.watchlist_add, name="watchlist"),
]
