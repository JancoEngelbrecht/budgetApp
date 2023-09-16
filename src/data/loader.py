import pandas as pd
import babel.dates
import datetime as dt
from functools import reduce, partial
from typing import Callable

class DataSchema:
    NAME = 'name'
    AMOUNT = "amount"
    VALUEDATE = "valuedate"
    CATEGORY = "category"
    MONTH = "month"
    YEAR = 'year'

# DATA PIPELINE
preprocessor = Callable[[pd.DataFrame], pd.DataFrame] # Callable input df and also return df

def create_year_column(df: pd.DataFrame) -> pd.DataFrame:
    df[DataSchema.YEAR] = df[DataSchema.VALUEDATE].dt.year.astype(str)
    return df

# TRANSLATE MONTH
def translate_date(df: pd.DataFrame) -> pd.DataFrame: # The arrow indicates the return type of the function
    def date_repr(date: dt.date) -> str:
        return babel.dates.format_date(date, format="MMMM")
    
    df[DataSchema.MONTH] = df[DataSchema.VALUEDATE].apply(date_repr)
    return df

def compose(*functions:preprocessor) -> preprocessor:
    return reduce(lambda f,g: lambda x: g(f(x)), functions)

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
    preprocessor = compose(
        create_year_column,
        partial(translate_date),
    )
    return preprocessor(data)


