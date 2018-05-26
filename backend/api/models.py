from django.db import models


class RawTxn(models.Model):
    balance = models.FloatField()
    external_id = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    sum = models.FloatField(default=0)
    date = models.DateField("Transaction Date")
    raw_txn_id = models.IntegerField()

    def __str__(self):
        return f"RawTxn(date={self.date}, sum={self.sum}, description={self.description}, " f"external_id={self.external_id} balance={self.balance}"


class ImportMetadata(models.Model):
    import_id = models.IntegerField()
    user_id = models.IntegerField()
    num_txns = models.IntegerField(default=0)
    source = models.CharField(max_length=200)
    datetime = models.DateTimeField("Import date and time")

    def __str__(self):
        return f"ImportMetadata(import_id={self.import_id}, date={self.datetime}, " f"source={self.source}, num_txns={self.num_txns}, user_id={self.user_id}"
