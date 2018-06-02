from django.conf.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r"transactions", views.TxnViewSet)
router.register(r"raw-transactions", views.RawTxnViewSet)
router.register(r"imports", views.ImportMetadataViewSet)

urlpatterns = [path("", include(router.urls))]
