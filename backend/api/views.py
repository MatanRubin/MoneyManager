from django.http import HttpResponse
from django.shortcuts import render_to_response
from rest_framework.reverse import reverse
from rest_framework import status, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import RawTxn, Txn, ImportMetadata
from .serializers import TxnSerializer, ImportMetadataSerializer, RawTxnSerializer
from .yahav_excel_data_importer import import_excel_file


@api_view(["GET"])
def api_root(request, format=None):
    return Response(
        {
            "transactions": reverse("transaction-list", request=request, format=format),
            # TODO make this work
            # 'transaction-detail': reverse('transaction-detail', kwargs={'pk': None}, request=request, format=format),
            "imports": reverse("import-list", request=request, format=format),
            "import": reverse("import", request=request, format=format),
        }
    )


class TxnViewSet(viewsets.ModelViewSet):

    queryset = Txn.objects.all()
    serializer_class = TxnSerializer


class RawTxnViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = RawTxn.objects.all()
    serializer_class = RawTxnSerializer


class ImportMetadataViewSet(viewsets.ModelViewSet):

    queryset = ImportMetadata.objects.all()
    serializer_class = ImportMetadataSerializer

    # def create(self, request, *args, **kwargs):
    #     # serializer.save(owner=self.request.user)
    #     import_metadata, raw_txns = import_excel_file(
    #         "/Users/maloni/Downloads/yahav.xls"
    #     )
    #     import_metadata.save()
    #     for raw_txn in raw_txns:
    #         raw_txn.import_metadata = import_metadata
    #         raw_txn.save()
    #         txn = Txn(
    #             raw_txn=raw_txn,
    #             balance=raw_txn.balance,
    #             external_id=raw_txn.external_id,
    #             description=raw_txn.description,
    #             sum=raw_txn.sum,
    #             date=raw_txn.date,
    #             comment="",
    #         )
    #         txn.save()
    #     new_serializer = ImportMetadataSerializer(import_metadata)
    #     return Response(new_serializer.data, status=status.HTTP_201_CREATED)
