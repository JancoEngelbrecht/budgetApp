from dash import Dash, html, dash_table
import pandas as pd

from src.components import (
    bar_chart,
    descrip_dropdown,
    month_dropdown,
    year_dropdown,
    bar_chart_two,
)

def create_layout(app: Dash, data: pd.DataFrame) -> html.Div:
    return html.Div(
        className="app-div",
        children=[
            html.H1(app.title),
            html.Hr(),
            dash_table.DataTable(data=data.to_dict('records'), page_size=10),
            html.Div(
                className='dropdown-container',
                children=[
                    year_dropdown.render(app, data),
                    month_dropdown.render(app, data),
                    descrip_dropdown.render(app, data)
                ]
            ),
            html.Div(
                className='bar-chart',
                children=[
                    bar_chart.render(app, data),
                    bar_chart_two.render(app, data),
                ]
            ),
        ]

    )