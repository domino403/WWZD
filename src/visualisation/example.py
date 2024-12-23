import pandas as pd
import holoviews as hv
import panel as pn
from holoviews import opts
import plotly.graph_objects as go
import numpy as np

# Ustawienie backendu na Plotly
hv.extension("plotly")

# Dane przykładowe
data = {
    "x": np.random.random(1000),
    "y": np.random.random(1000),
    "z": np.random.random(1000),
}
df = pd.DataFrame(data)

# Tworzenie widgetu do zmiany wielkości punktów
point_size_slider = pn.widgets.IntSlider(
    name="Wielkość punktów", start=1, end=20, step=1, value=2
)


# Funkcja do aktualizacji wykresu
@pn.depends(point_size_slider)
def update_scatter(point_size):
    scatter_3d = hv.Scatter3D((df["x"], df["y"], df["z"])).opts(
        opts.Scatter3D(
            size=point_size,
            color="blue",
            width=1840,
            height=1080,
            title="Interaktywny wykres 3D z Plotly",
        )
    )

    # Eksportujemy do obiektu Plotly Figure
    plotly_dict = hv.render(scatter_3d, backend="plotly")

    # Konwersja dict do obiektu Figure
    plotly_fig = go.Figure(plotly_dict)

    # Modyfikacja wykresu - ukrywanie osi
    plotly_fig.update_scenes(
        xaxis_visible=False, yaxis_visible=False, zaxis_visible=False
    )

    return plotly_fig


# Tworzenie aplikacji Panel
dashboard = pn.Column(
    "# Interaktywny raport z wykresem 3D",
    "### Użyj suwaka, aby zmienić wielkość punktów:",
    point_size_slider,
    pn.panel(update_scatter),
)

# Zapis do pliku HTML
dashboard.save("raport_interaktywny_plotly.html", embed=True)
