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


class Txn(models.Model):
    raw_txn = models.OneToOneField(RawTxn, on_delete=models.CASCADE)
    comment = models.CharField(max_length=1000, blank=True)


class ImportMetadata(models.Model):
    num_txns = models.IntegerField(default=0)
    source = models.CharField(max_length=200)
    datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (
            f"ImportMetadata(id={self.id}, date={self.datetime}, source={self.source}, num_txns={self.num_txns})"
        )
