from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import RawTxn
from .serializers import RawTxnSerializer
from .yahav_excel_txn_importer.yahav_excel_data_importer import import_excel_file


def index(request):
    return HttpResponse("Hello, world!")


@api_view(["GET"])
def list_txns(request, format=None):
    txns = RawTxn.objects.all()
    serializer = RawTxnSerializer(txns, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def txn_details(request, txn_id, format=None):
    try:
        txn = RawTxn.objects.get(pk=txn_id)
    except RawTxn.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = RawTxnSerializer(txn)
        return Response(serializer.data)


# TODO make this a POST and get an actual file
@api_view(["GET"])
def import_excel(request, format=None):
    import_metadata, txns = import_excel_file("/Users/maloni/Downloads/yahav.xls")
    raw_txns = [
        RawTxn(
            balance=x.balance,
            external_id=x.external_id,
            description=x.description,
            sum=x.sum,
            date=x.date,
        )
        for x in txns
    ]
    for raw_txn in raw_txns:
        raw_txn.save()
    # TODO persist import_metadata
    serializer = RawTxnSerializer(raw_txns, many=True)
    return Response(serializer.data, status=status.HTTP_201_CREATED)
