from dash import Dash, dcc, html
from . import ids
from dash.dependencies import Input, Output
import pandas as pd
from ..data.loader import DataSchema
import plotly.express as px


def render(app: Dash, data: pd.DataFrame) -> html.Div:
    @app.callback(
        Output(ids.BAR_CHART_TWO, 'children'),
        [Input(ids.YEAR_DROPDOWN_TWO, 'value'),
         Input(ids.MONTH_DROPDOWN_TWO, 'value'),
         Input(ids.DESCRIP_DROPDOWN, 'value')]
    )

    def update_bar_chart(years: list[str], months: list[str], categorys: list[str]) -> html.Div:
        filtered_data = data.query('year in @years and month in @months and category in @categorys')

        if filtered_data.shape[0] == 0:
            return html.Div('No data selected.')
        
        def create_pivot_table() -> pd.DataFrame:
            pt = filtered_data.pivot_table(
                values=DataSchema.AMOUNT, 
                index=[DataSchema.MONTH],
                aggfunc='sum',
                fill_value=0
            )
            return pt.reset_index().sort_values(DataSchema.AMOUNT, ascending=False)

        fig = px.bar(
            create_pivot_table(),
            x = DataSchema.MONTH,
            y = DataSchema.AMOUNT,
            color=DataSchema.MONTH
        )
        return html.Div(dcc.Graph(figure=fig), id=ids.BAR_CHART_TWO)
    return html.Div(id=ids.BAR_CHART_TWO)