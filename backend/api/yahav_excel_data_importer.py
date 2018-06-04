# coding=utf-8
from typing import List
import pandas as pd

from .models import RawTxn, ImportMetadata


def import_excel_file(input_file) -> (ImportMetadata, List[RawTxn]):
    xl = pd.ExcelFile(input_file)
    data_frame = xl.parse(
        'תנועות עו"ש',
        header=5,
        usecols="A:E,G",
        names=["balance", "incoming", "outgoing", "description", "external_id", "date"],
    )

    txns = []
    for index, row in data_frame.iterrows():
        sum = row["incoming"] - row["outgoing"]
        txns.append(
            RawTxn(
                balance=row["balance"],
                external_id=row["external_id"],
                description=row["description"],
                sum=sum,
                date=row["date"],
            )
        )
    import_metadata = ImportMetadata(
        num_txns=len(txns), source=input_file, file=input_file
    )
    return import_metadata, txns
