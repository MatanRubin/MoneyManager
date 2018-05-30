from rest_framework import serializers
from .models import RawTxn, ImportMetadata, Txn


class RawTxnSerializer(serializers.HyperlinkedModelSerializer):

    def create(self, validated_data):
        return RawTxn.objects.create(**validated_data)

    class Meta:
        model = RawTxn
        fields = ("id", "balance", "external_id", "description", "sum", "date")


class TxnSerializer(serializers.HyperlinkedModelSerializer):

    raw_txn = RawTxnSerializer(read_only=True)

    def create(self, validated_data):
        return Txn.objects.create(**validated_data)

    class Meta:
        model = Txn
        fields = ("id", "raw_txn", "comment")


class ImportMetadataSerializer(serializers.HyperlinkedModelSerializer):

    def create(self, validated_data):
        return ImportMetadata.objects.create(**validated_data)

    class Meta:
        model = ImportMetadata
        fields = ("num_txns", "source", "datetime")
