from rest_framework import serializers
from .models import RawTxn, ImportMetadata


class RawTxnSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        return RawTxn.objects.create(**validated_data)

    class Meta:
        model = RawTxn
        fields = ("id", "balance", "external_id", "description", "sum", "date")
