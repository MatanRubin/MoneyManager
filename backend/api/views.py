from django.http import HttpResponse
from django.shortcuts import render_to_response
from rest_framework.reverse import reverse
from rest_framework import status
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


class TxnList(APIView):
    """
    List all transactions, or create/edit/delete a transaction
    """

    def get(self, request, format=None):
        txns = Txn.objects.all()
        serializer = TxnSerializer(txns, context={"request": request}, many=True)
        return Response(serializer.data)


class TxnDetails(APIView):

    def get_object(self, pk):
        try:
            return Txn.objects.get(pk=pk)
        except Txn.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk, format=None):
        txn = self.get_object(pk)
        serializer = TxnSerializer(txn, context={"request": request})
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        txn = self.get_object(pk)
        txn.comment = request.data["comment"]
        txn.save()
        serializer = TxnSerializer(txn, context={"request": request})
        return Response(serializer.data)


class RawTxnDetails(APIView):

    def get_object(self, pk):
        try:
            return RawTxn.objects.get(pk=pk)
        except Txn.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk, format=None):
        raw_txn = self.get_object(pk)
        serializer = RawTxnSerializer(raw_txn, context={"request": request})
        return Response(serializer.data)


class ImportMetadataList(APIView):

    def get(self, request, format=None):
        imports = ImportMetadata.objects.all()
        serializer = ImportMetadataSerializer(imports, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        import_metadata, raw_txns = import_excel_file(
            "/Users/maloni/Downloads/yahav.xls"
        )
        import_metadata.save()
        for raw_txn in raw_txns:
            raw_txn.import_metadata = import_metadata
            raw_txn.save()
            txn = Txn(
                raw_txn=raw_txn,
                balance=raw_txn.balance,
                external_id=raw_txn.external_id,
                description=raw_txn.description,
                sum=raw_txn.sum,
                date=raw_txn.date,
                comment="",
            )
            txn.save()
        serializer = ImportMetadataSerializer(import_metadata)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ImportMetadataDetails(APIView):

    def get_object(self, pk):
        try:
            return ImportMetadata.objects.get(pk=pk)
        except Txn.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk, format=None):
        import_metadata = self.get_object(pk)
        serializer = ImportMetadataSerializer(import_metadata)
        return Response(serializer.data)
