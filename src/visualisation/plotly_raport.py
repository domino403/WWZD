import os
import polars as pl
import plotly.graph_objects as go
import dash
from dash import dcc, html, Input, Output, State
from PIL import Image

from logging_config import setup_logger
from src.data_transformation.dim_reduction import (
    pca_dim_reduction,
    t_sne_dim_reduction,
    truncated_svd_dim_reduction,
)

LOGGER = setup_logger()


class VisualizationApp:
    def __init__(
        self,
        data: pl.DataFrame,
        x_col: str,
        y_col: str,
        z_col: str,
        id_col: str,
        images_dir: str,
    ):
        self.DataFrame = data
        self.data = pca_dim_reduction(self.DataFrame, 3).head(100)
        self.x_col = x_col
        self.y_col = y_col
        self.z_col = z_col
        self.id_col = id_col
        self.images_dir = images_dir
        self.max_data_count = self.DataFrame.height
        self.range_start = 0
        self.range_end = 100
        self.data_set_name = "PCA top 100"
        self.fig = self.create_scatter3d_figure()
        self.app = self.create_dash_app()

    def update_data(self, new_range: tuple[int, int], red_method: str) -> None:
        self.range_start, self.range_end = new_range
        self.data_set_name = f"{red_method} DATA {self.range_start}-{self.range_end}"
        if red_method == "PCA":
            self.data = pca_dim_reduction(self.DataFrame, 3).slice(
                self.range_start, self.range_end - self.range_start
            )
        elif red_method == "T_sne":
            self.data = t_sne_dim_reduction(self.DataFrame, 3).slice(
                self.range_start, self.range_end - self.range_start
            )
        elif red_method == "SVD":
            self.data = truncated_svd_dim_reduction(self.DataFrame, 3).slice(
                self.range_start, self.range_end - self.range_start
            )

        self.fig = self.create_scatter3d_figure()

    def create_scatter3d_figure(self):
        image_paths = [
            os.path.join(self.images_dir, img_id) for img_id in self.data[self.id_col]
        ]
        fig = go.Figure(
            data=[
                go.Scatter3d(
                    x=self.data[self.x_col],
                    y=self.data[self.y_col],
                    z=self.data[self.z_col],
                    mode="markers",
                    marker=dict(size=5, color="blue"),
                    customdata=image_paths,
                    text=self.data[self.id_col],
                    hovertemplate="<b>%{text}</b>",
                )
            ]
        )
        return fig

    def create_dash_app(self):
        app = dash.Dash(__name__)

        app.layout = html.Div(
            [
                html.Div(
                    [
                        html.H3("Current Data Set:"),
                        html.Div(id="data-set-name", children=self.data_set_name),
                        html.Br(),
                        html.Br(),
                        html.Label(
                            f"Select Data id Range: ({0}-{self.max_data_count-1})"
                        ),
                        html.Div(
                            [
                                dcc.Input(
                                    id="range-start",
                                    type="number",
                                    value=self.range_start,
                                    min=0,
                                    max=self.max_data_count,
                                    style={"width": "100px"},
                                ),
                                dcc.Input(
                                    id="range-end",
                                    type="number",
                                    value=self.range_end,
                                    min=0,
                                    max=self.max_data_count,
                                    style={"width": "100px"},
                                ),
                            ],
                            style={"display": "flex", "gap": "7px"},
                        ),
                        html.Br(),
                        html.Br(),
                        html.Br(),
                        html.Label("Select Dimension Reduction Method:"),
                        dcc.RadioItems(
                            id="dimension-reduction-method",
                            options=[
                                {"label": "PCA", "value": "PCA"},
                                {"label": "T_sne", "value": "T_sne"},
                                {"label": "Truncated SVD", "value": "SVD"},
                            ],
                            value="PCA",
                            labelStyle={
                                "display": "inline-block",
                                "margin-right": "10px",
                            },
                        ),
                        html.Button("Update", id="update-button", n_clicks=0),
                    ],
                    style={
                        "width": "20%",
                        "display": "inline-block",
                        "vertical-align": "top",
                    },
                ),
                html.Div(
                    [
                        dcc.Loading(
                            id="loading-spinner",
                            type="circle",
                            children=[
                                dcc.Graph(id="scatter3d", figure=self.fig),
                                html.Div(id="output-text"),
                            ],
                        )
                    ],
                    style={
                        "width": "75%",
                        "display": "inline-block",
                        "padding-left": "5%",
                    },
                ),
            ]
        )

        @app.callback(
            [Output("range-start", "value"), Output("range-end", "value")],
            [Input("range-start", "value"), Input("range-end", "value")],
        )
        def sync_inputs(start_value, end_value):
            ctx = dash.callback_context
            if not ctx.triggered:
                raise dash.exceptions.PreventUpdate

            input_id = ctx.triggered[0]["prop_id"].split(".")[0]

            if input_id == "range-start":
                return start_value, end_value
            elif input_id == "range-end":
                return start_value, end_value

        @app.callback(
            [
                Output("scatter3d", "figure"),
                Output("output-text", "children"),
                Output("data-set-name", "children"),
            ],
            [Input("update-button", "n_clicks"), Input("scatter3d", "clickData")],
            [
                State("range-start", "value"),
                State("range-end", "value"),
                State("dimension-reduction-method", "value"),
                State("scatter3d", "relayoutData"),
            ],
        )
        def update_figure(
            n_clicks, clickData, start_value, end_value, method, relayoutData
        ):
            ctx = dash.callback_context

            if not ctx.triggered:
                raise dash.exceptions.PreventUpdate

            trigger = ctx.triggered[0]["prop_id"].split(".")[0]

            if trigger == "update-button":
                self.update_data((start_value, end_value), method)

                new_fig = self.fig  # Use the updated figure

                if relayoutData and "scene.camera" in relayoutData:
                    new_fig.update_layout(scene_camera=relayoutData["scene.camera"])

                return new_fig, html.Div(), self.data_set_name

            elif trigger == "scatter3d":
                if clickData is None:
                    return (
                        self.fig,
                        "Kliknij punkt na wykresie, aby zobaczyć szczegóły tutaj.",
                        self.data_set_name,
                    )

                LOGGER.info(clickData["points"][0])
                point_index = clickData["points"][0].get("pointNumber", None)

                if point_index is None:
                    return (
                        self.fig,
                        "Nie można znaleźć indeksu punktu.",
                        self.data_set_name,
                    )

                new_fig = self.fig
                new_marker_colors = ["blue"] * len(self.data)
                new_marker_colors[point_index] = "red"
                new_fig["data"][0]["marker"]["color"] = new_marker_colors

                if relayoutData and "scene.camera" in relayoutData:
                    new_fig.update_layout(scene_camera=relayoutData["scene.camera"])

                point_name = self.data[self.id_col][point_index]
                image_path = os.path.join(self.images_dir, point_name)
                LOGGER.info(image_path)
                image_element = html.Img(src=Image.open(image_path))

                return new_fig, image_element, self.data_set_name

        return app
