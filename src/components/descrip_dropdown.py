from dash import Dash, html, dcc
from dash.dependencies import Input, Output
from . import ids
import pandas as pd
from src.data.loader import DataSchema





def render(app: Dash, data: pd.DataFrame) -> html.Div:
    all_descrip: list[str] = data[DataSchema.DESCRIP].tolist()
    unique_descrip: list[str] = sorted(set(all_descrip))

    @app.callback(
        Output(ids.DESCRIP_DROPDOWN, 'value'),
        [Input(ids.YEAR_DROPDOWN, 'Value'),
         Input(ids.MONTH_DROPDOWN, 'Value'),
         Input(ids.SELECT_ALL_DESCRIP_BUTTON, 'n_clicks')]
    )

    def select_all_descrip(years: list[str], months: list[str] , _: int) -> list[str]:
        filtered_data = data.query('year in @years and month in @months')
        return sorted(set(filtered_data[DataSchema.DESCRIP].tolist()))

    return html.Div(
        children=[
            html.H6("Months"),
            dcc.Dropdown(
                id=ids.DESCRIP_DROPDOWN,
                options=[{"label": descrip, "value": descrip} for descrip in unique_descrip],
                value= unique_descrip,
                multi=True
            ), 
            html.Button(
                className='dropdown-button',
                children=['Select All'],
                id=ids.SELECT_ALL_DESCRIP_BUTTON,
                n_clicks=0,
            ),  
        ]
    )

