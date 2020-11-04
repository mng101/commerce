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
    path("watchlist/", views.WatchlistListView.as_view(), name="watchlist"),
    path("categorylist/", views.CategoryListView.as_view(), name="categorylist"),
    path('<int:pk>/', views.ListingDetailView.as_view(), name="detail"),
    path('update/<int:pk>/', views.ListingUpdateView.as_view(), name="update"),
    path('close/<int:pk>/', views.close, name="close"),
    path('bid/<int:pk>/', views.BidCreateView.as_view(), name="bid"),
    path('comment/<int:pk>/', views.CommentCreateView.as_view(), name="comment"),
    path('add2watchlist/<int:pk>/', views.add2watchlist, name="add2watchlist"),
    path('removewatchlist/<int:pk>/', views.removewatchlist, name="removewatchlist"),
]
