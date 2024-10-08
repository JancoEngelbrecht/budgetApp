from dash import Dash, html, dcc
from dash.dependencies import Input, Output
from . import ids
import pandas as pd
from src.data.loader import DataSchema





def render(app: Dash, data: pd.DataFrame) -> html.Div:
    all_years: list[str] = data[DataSchema.YEAR].tolist()
    unique_years = sorted(set(all_years), key=int)

    @app.callback(
        Output(ids.YEAR_DROPDOWN_TWO, 'value'),
        Input(ids.SELECT_ALL_YEAR_BUTTON_TWO, 'n_clicks'),
    )
    def select_all_descrip(_: int) -> list[str]:
        return unique_years

    return html.Div(
        children=[
            html.H6("Year"),
            dcc.Dropdown(
                id=ids.YEAR_DROPDOWN_TWO,
                options=[{"label": year, "value": year} for year in unique_years],
                value= unique_years,
                multi=True
            ), 
            html.Button(
                className='dropdown-button',
                children=['Select All'],
                id=ids.SELECT_ALL_YEAR_BUTTON_TWO,
                n_clicks=0,
            ),  
        ]
    )

