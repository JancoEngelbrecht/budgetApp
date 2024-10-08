from dash import Dash, html, dcc
from dash.dependencies import Input, Output
from . import ids
import pandas as pd
from src.data.loader import DataSchema





def render(app: Dash, data: pd.DataFrame) -> html.Div:
    all_months: list[str] = data[DataSchema.MONTH].tolist()
    unique_months = sorted(set(all_months))

    @app.callback(
        Output(ids.MONTH_DROPDOWN, 'value'),
        [Input(ids.YEAR_DROPDOWN, 'value'),Input(ids.SELECT_ALL_MONTH_BUTTON, 'n_clicks')]
    )
    def select_all_months(years: list[str], _:int) -> list[str]:
        filtered_data = data.query('year in @years')
        return sorted(set(filtered_data[DataSchema.MONTH].tolist()))

    return html.Div(
        children=[
            html.H6("Months"),
            dcc.Dropdown(
                id=ids.MONTH_DROPDOWN,
                options=[{"label": month, "value": month} for month in unique_months],
                value= unique_months,
                multi=True,
            ), 
            html.Button(
                className='dropdown-button',
                children=['Select All'],
                id=ids.SELECT_ALL_MONTH_BUTTON,
                n_clicks=0,
            ),  
        ]
    )

