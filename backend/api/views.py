from django.http import HttpResponse
from django.shortcuts import render_to_response
from rest_framework.reverse import reverse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import RawTxn, Txn, ImportMetadata
from .serializers import TxnSerializer, ImportMetadataSerializer
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


@api_view(["GET"])
def list_txns(request, format=None):
    txns = Txn.objects.all()
    serializer = TxnSerializer(txns, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def txn_details(request, txn_id, format=None):
    try:
        txn = Txn.objects.get(pk=txn_id)
    except Txn.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    serializer = TxnSerializer(txn)
    return Response(serializer.data)


# TODO make this a POST and get an actual file
@api_view(["GET"])
def import_excel(request, format=None):
    import_metadata, raw_txns = import_excel_file("/Users/maloni/Downloads/yahav.xls")
    for raw_txn in raw_txns:
        raw_txn.save()
        txn = Txn(raw_txn=raw_txn, comment="")
        txn.save()
    import_metadata.save()
    serializer = ImportMetadataSerializer(import_metadata)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["GET"])
def import_list(request, format=None):
    imports = ImportMetadata.objects.all()
    serializer = ImportMetadataSerializer(imports, many=True)
    return Response(serializer.data)
