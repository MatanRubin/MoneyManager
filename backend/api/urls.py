from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from . import views


urlpatterns = [
    path("", views.api_root),
    path("transactions", views.TxnList.as_view(), name="transaction-list"),
    path(
        "transactions/<int:pk>", views.TxnDetails.as_view(), name="transaction-detail"
    ),
    path(
        "raw-transactions/<int:pk>",
        views.RawTxnDetails.as_view(),
        name="raw-transaction-detail",
    ),
    path("imports", views.ImportMetadataList.as_view(), name="import-list"),
    path(
        "imports/<int:pk>",
        views.ImportMetadataDetails.as_view(),
        name="import-metadata-detail",
    ),
]

urlpatterns = format_suffix_patterns(urlpatterns)
