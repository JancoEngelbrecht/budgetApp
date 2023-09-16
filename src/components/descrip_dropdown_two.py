from dash import Dash, html, dcc
from dash.dependencies import Input, Output
from . import ids
import pandas as pd
from src.data.loader import DataSchema

# Data = Load_transaction Data | App = Dash
def render(app, data):
    all_descrip = data[DataSchema.CATEGORY].tolist()
    unique_descrip = sorted(set(all_descrip))

 # When input changes, the output should update
 # Id must be the same as the Id give in layout
 # @callback needs to be right above teh function to work. 
    @app.callback(
        Output(ids.DESCRIP_DROPDOWN_TWO, 'value'),
        [Input(ids.YEAR_DROPDOWN_TWO, 'value'),
         Input(ids.MONTH_DROPDOWN_TWO, 'value'),
         Input(ids.SELECT_ALL_DESCRIP_BUTTON_TWO, 'n_clicks')],
    )
    def select_all_descrip(years, months, _:int):
        filtered_data_two = data.query('year in @years and month in @months')
        return sorted(set(filtered_data_two[DataSchema.CATEGORY].tolist()))

    return html.Div(
        children=[
            html.H6("Descriptions"),
            dcc.Dropdown(
                id=ids.DESCRIP_DROPDOWN_TWO,
                options=[{"label": descrip, "value": descrip} for descrip in unique_descrip],
                value= unique_descrip, # Default Value
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

