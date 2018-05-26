# coding=utf-8
from typing import List

import pandas as pd
import pendulum
from pendulum import UTC


class ImportMetadata:

    def __init__(
        self,
        import_id: int,
        datetime: pendulum.DateTime,
        source: str,
        num_txns: int,
        user_id: int,
    ):
        self.user_id = user_id
        self.num_txns = num_txns
        self.source = source
        self.datetime = datetime
        self.import_id = import_id

    def __repr__(self) -> str:
        return f"ImportMetadata(import_id={self.import_id}, date={self.datetime}, " f"source={self.source}, num_txns={self.num_txns}, user_id={self.user_id}"


class RawTxn:

    def __init__(
        self,
        date: pendulum.Date,
        sum: float,
        description: str,
        external_id: str,
        balance: float,
    ):
        self.balance = balance
        self.external_id = external_id
        self.description = description
        self.sum = sum
        self.date = date
        self.raw_txn_id = None

    def __repr__(self):
        return f"RawTxn(date={self.date}, sum={self.sum}, description={self.description}, " f"external_id={self.external_id} balance={self.balance}"


def import_excel_file(input_path: str) -> (ImportMetadata, List[RawTxn]):
    xl = pd.ExcelFile(input_path)
    data_frame = xl.parse(
        'תנועות עו"ש',
        header=5,
        usecols="A:E,G",
        names=["balance", "incoming", "outgoing", "description", "external_id", "date"],
    )

    txns = []
    for index, row in data_frame.iterrows():
        sum = row.incoming - row.outgoing
        txns.append(
            RawTxn(
                pendulum.parse(str(row.date)).date(),
                sum,
                row.description,
                row.external_id,
                row.balance,
            )
        )
    import_metadata = ImportMetadata(
        None, pendulum.now(UTC), input_path, len(txns), None
    )
    return import_metadata, txns


if __name__ == "__main__":
    import_metadata, raw_txns = import_excel_file("/Users/maloni/Downloads/yahav.xls")
    print("hello")
