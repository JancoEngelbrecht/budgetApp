from dash import Dash, html, dcc
from dash.dependencies import Input, Output
from . import ids
import pandas as pd
from src.data.loader import DataSchema





def render(app: Dash, data: pd.DataFrame) -> html.Div:
    all_descrip: list[str] = data[DataSchema.CATEGORY].tolist()
    unique_descrip: list[str] = sorted(set(all_descrip))

    @app.callback(
        Output(ids.DESCRIP_DROPDOWN_TWO, 'value'),
        [Input(ids.YEAR_DROPDOWN_TWO, 'value'),
         Input(ids.MONTH_DROPDOWN_TWO, 'value'),
         Input(ids.SELECT_ALL_DESCRIP_BUTTON_TWO, 'n_clicks')],
    )

    def select_all_descrip(years: list[str], months: list[str] , _: int) -> list[str]:
        filtered_data_two = data.query('year in @years and month in @months')
        return sorted(set(filtered_data_two[DataSchema.CATEGORY].tolist()))

    return html.Div(
        children=[
            html.H6("Descriptions"),
            dcc.Dropdown(
                id=ids.DESCRIP_DROPDOWN_TWO,
                options=[{"label": descrip, "value": descrip} for descrip in unique_descrip],
                value= unique_descrip,
                multi=True,
                placeholder="Select"
            ), 
            html.Button(
                className='dropdown-button',
                children=['Select All'],
                id=ids.SELECT_ALL_DESCRIP_BUTTON_TWO,
                n_clicks=0,
            ),  
        ]
    )

