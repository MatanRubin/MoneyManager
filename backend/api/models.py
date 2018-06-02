from django.db import models


class ImportMetadata(models.Model):
    num_txns = models.IntegerField(default=0)
    source = models.CharField(max_length=200)
    datetime = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to="imports", default="imports/None.xls")

    def __str__(self):
        return (
            f"ImportMetadata(id={self.id}, date={self.datetime}, source={self.source}, num_txns={self.num_txns})"
        )


class RawTxn(models.Model):
    import_metadata = models.ForeignKey(ImportMetadata, on_delete=models.CASCADE)
    balance = models.FloatField()
    external_id = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    sum = models.FloatField(default=0)
    date = models.DateField("Transaction Date")

    def __str__(self):
        return (
            f"RawTxn(id={self.id}, import_metadata_id={self.import_metadata.id}, date={self.date}, sum={self.sum}, description={self.description}, external_id={self.external_id}, balance={self.balance})"
        )


class Txn(models.Model):
    raw_txn = models.OneToOneField(RawTxn, on_delete=models.CASCADE)
    balance = models.FloatField()
    external_id = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    sum = models.FloatField(default=0)
    date = models.DateField("Transaction Date")
    comment = models.CharField(max_length=1000, blank=True)

    def __str__(self):
        return (
            f"Txn(id={self.id}, raw_txn_id={raw_txn.id}, date={self.date}, sum={self.sum}, description={self.description}, external_id={self.external_id}, balance={self.balance})"
        )
