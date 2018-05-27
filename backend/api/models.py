from django.db import models


class RawTxn(models.Model):
    balance = models.FloatField()
    external_id = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    sum = models.FloatField(default=0)
    date = models.DateField("Transaction Date")

    def __str__(self):
        return (
            f"RawTxn(id={self.id}, date={self.date}, sum={self.sum}, description={self.description}, external_id={self.external_id}, balance={self.balance})"
        )


class ImportMetadata(models.Model):
    user_id = models.IntegerField()
    num_txns = models.IntegerField(default=0)
    source = models.CharField(max_length=200)
    datetime = models.DateTimeField("Import date and time")

    def __str__(self):
        return (
            f"ImportMetadata(id={self.id}, date={self.datetime}, source={self.source}, num_txns={self.num_txns}, user_id={self.user_id})"
        )
