import pandas as pd
import json
import plotly
import plotly.express as px
import plotly.graph_objects as go




def plot_locations(lat, lon, locations):
    """
    Generate a Plotly figure and convert it to a JSON string.
    Uses sample data from gapminder as an example.
    """
    import plotly.graph_objects as go

    fig = go.Figure(go.Scattergeo())
    fig.add_scattergeo(lat = lat
                      ,lon = lon
                      ,text= locations
                      ,hovertext = locations
                      ,hoverinfo="text"
                      ,marker_size = 10)
    fig.update_geos(projection_type="natural earth", resolution = 50, landcolor="#26A69A", showcountries=True)
    fig.update_layout(
        height=420,
        margin={"r":0,"t":0,"l":0,"b":0},
        hoverlabel=dict(
        bgcolor="white",
        font_size=25,
        font_color = "#26A69A"
    ))
    

    data_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return data_json



