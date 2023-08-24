from dash import Dash, dcc, html
from . import ids
from dash.dependencies import Input, Output
import pandas as pd
from ..data.loader import DataSchema
import plotly.graph_objects as go



def render(app: Dash, data: pd.DataFrame) -> html.Div:
    @app.callback(
        Output(ids.PIE_CHART, 'children'),
        [Input(ids.YEAR_DROPDOWN, 'value'),
         Input(ids.MONTH_DROPDOWN, 'value'),
         Input(ids.DESCRIP_DROPDOWN, 'value')]
    )

    def update_pie_chart(years: list[str], months: list[str], descrips: list[str]) -> html.Div:
        filtered_data = data.query('year in @years and month in @months and descrip in @descrips')

        if filtered_data.shape[0] == 0:
            return html.Div('No data selected.', id = ids.PIE_CHART)
        
        pie = go.Pie(
            labels = filtered_data[DataSchema.DESCRIP].tolist(),
            values=filtered_data[DataSchema.AMOUNT].tolist(),
            hole=0.1,
        )

        fig = go.Figure(data=[pie])
        fig.update_layout(margin={"t":40, "b": 0, "l": 0, "r": 0})
        fig.update_traces(hovertemplate='%{label}<br>$%{value:.2f}<extra></extra>')

        return html.Div(dcc.Graph(figure=fig), id=ids.PIE_CHART)
    return html.Div(id=ids.PIE_CHART)