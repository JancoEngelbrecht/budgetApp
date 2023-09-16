from dash import Dash, html, dcc
from dash.dependencies import Input, Output
from . import ids
import pandas as pd
from src.data.loader import DataSchema



def render(app: Dash, data: pd.DataFrame) -> html.Div:
    all_years: list[str] = data[DataSchema.YEAR].tolist()
    unique_years = sorted(set(all_years), key=int)

    @app.callback(
        Output(ids.YEAR_DROPDOWN, 'value'),
        Input(ids.SELECT_ALL_YEAR_BUTTON, 'n_clicks'), 
        # When the state of "n_clicks" changes, then it runs the function "select_all_years".
        # This updates the value linked with the ID. 
        # The value parameter in Year dropdow then gets overwritten. 
    )
    def select_all_years(_: int) -> list[str]: # This Function is linked to the callback 
        return unique_years # ['2022', '2023']

    return html.Div(
        children=[
            html.H6("Year"),
            dcc.Dropdown(
                id=ids.YEAR_DROPDOWN,
                options=[{"label": year, "value": year} for year in unique_years], # This is a for loop Year iterates through unique_years 
                value= unique_years,
                multi=True
            ), 
            html.Button(
                className='dropdown-button',
                children=['Select All'],
                id=ids.SELECT_ALL_YEAR_BUTTON,
                n_clicks=0,
            ),  
        ]
    )
