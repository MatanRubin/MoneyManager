from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from . import views


urlpatterns = [
    path("transactions", views.list_txns),
    path("transactions/<int:pk>", views.txn_details),
    path("commands/import", views.import_excel),
]

urlpatterns = format_suffix_patterns(urlpatterns)
