from django.urls import path, include
from . import views
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    # Public API endpoints
    # Tips endpoints
    path("api/tips/", views.TipListView.as_view(), name="tip-list-create"),
    path("api/tips/<int:tip_id>/", views.TipDetailView.as_view(), name="tip-detail"),
    # Voting endpoint (existing)
    path("api/tips/<int:tip_id>/vote/", views.tip_vote, name="tip-vote"),
    # Tip creation endpoint (existing)
    path("api/tips/create/", views.create_tip, name="tip-create"),
    # Flagging endpoint (existing)
    path("api/tips/<int:tip_id>/flag/", views.flag_content, name="tip-flag"),
    # Category endpoints
    path("api/categories/", views.CategoryListView.as_view(), name="category-list"),
    path(
        "api/categories/<slug:slug>/",
        views.CategoryDetailView.as_view(),
        name="category-detail",
    ),
    # Products endpoint
    path("api/products/", views.AffiliateProductList.as_view(), name="product-list"),
    # Search endpoint
    path("api/tips/search/", views.search_tips, name="tip-search"),
]
