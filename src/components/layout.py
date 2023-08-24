from dash import Dash, html
from . import bar_chart
from . import pie_chart
import pandas as pd

from . import descrip_dropdown
from . import year_dropdown
from . import month_dropdown

def create_layout(app: Dash, data: pd.DataFrame) -> html.Div:
    return html.Div(
        className="app-div",
        children=[
            html.H1(app.title),
            html.Hr(),
            html.Div(
                className='dropdown-container',
                children=[
                    year_dropdown.render(app, data),
                    month_dropdown.render(app, data),
                    descrip_dropdown.render(app, data)
                ]
            ),
            bar_chart.render(app, data),
        ]

    )