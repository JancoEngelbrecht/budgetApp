import pandas as pd

class DataSchema:
    NAME = 'name'
    AMOUNT = "amount"
    VALUEDATE = "valuedate"
    CATEGORY = "category"
    MONTH = "month"
    YEAR = 'year'



def load_transaction_data(path: str) -> pd.DataFrame:
    # load the data from a CSV file
    data = pd.read_csv(
        path,
        dtype={
            DataSchema.AMOUNT: float,
            DataSchema.NAME: str,
            DataSchema.CATEGORY: str,
            },
            parse_dates=[DataSchema.VALUEDATE]
    )
    data[DataSchema.YEAR] = data[DataSchema.VALUEDATE].dt.year.astype(str)
    data[DataSchema.MONTH] = data[DataSchema.VALUEDATE].dt.month.astype(str)
    return data