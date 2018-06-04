from rest_framework import serializers
from rest_framework.relations import HyperlinkedRelatedField

from .models import RawTxn, ImportMetadata, Txn


class RawTxnSerializer(serializers.HyperlinkedModelSerializer):

    import_metadata = HyperlinkedRelatedField(
        read_only=True, view_name="import-metadata-detail"
    )

    def create(self, validated_data):
        return RawTxn.objects.create(**validated_data)

    class Meta:
        model = RawTxn
        fields = (
            "id",
            "import_metadata",
            "balance",
            "external_id",
            "description",
            "sum",
            "date",
        )


class TxnSerializer(serializers.ModelSerializer):

    raw_txn = HyperlinkedRelatedField(
        read_only=True, view_name="raw-transaction-detail"
    )

    def create(self, validated_data):
        return Txn.objects.create(**validated_data)

    class Meta:
        model = Txn
        fields = (
            "id",
            "raw_txn",
            "balance",
            "external_id",
            "description",
            "sum",
            "date",
            "comment",
        )


class ImportMetadataSerializer(serializers.HyperlinkedModelSerializer):

    file = serializers.FileField(max_length=None, use_url=True)

    def create(self, validated_data):
        return ImportMetadata.objects.create(**validated_data)

    class Meta:
        model = ImportMetadata
        fields = ("num_txns", "source", "datetime", "file")
        read_only_fields = ("num_txns", "source")
