import pandas as pd

class DataSchema:
    ACCOUNTNUMBER = "accountnumber"
    CURRANCY = "currancy"
    STARTSALDO = "startsaldo"
    ENDSALDO = "endsaldo"
    AMOUNT = "amount"
    DESCRIP = "descrip"
    TRANSACTIONDATE = "transactiondate"
    VALUEDATE = "valuedate"
    MONTH = "month"
    YEAR = 'year'



def load_transaction_data(path: str) -> pd.DataFrame:
    # load the data from a CSV file
    data = pd.read_csv(
        path,
        dtype={
            DataSchema.ACCOUNTNUMBER: int,
            DataSchema.CURRANCY: str,
            DataSchema.STARTSALDO: float,
            DataSchema.ENDSALDO: float,
            DataSchema.AMOUNT: float,
            DataSchema.DESCRIP: str,
            },
            parse_dates=[DataSchema.VALUEDATE,DataSchema.TRANSACTIONDATE]
    )
    data[DataSchema.YEAR] = data[DataSchema.VALUEDATE].dt.year.astype(str)
    data[DataSchema.MONTH] = data[DataSchema.VALUEDATE].dt.month.astype(str)
    return data