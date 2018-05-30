from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from . import views


urlpatterns = [
    path("", views.api_root),
    path("transactions", views.list_txns, name="transaction-list"),
    path("transactions/<int:pk>", views.txn_details, name="transaction-detail"),
    path("commands/import", views.import_excel, name="import"),
    path("imports", views.import_list, name="import-list"),
]

urlpatterns = format_suffix_patterns(urlpatterns)
