#DASH with PLOTLY
#Dashboarding with Dash and Plotyl - intro
import dash
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
import pandas as pd
import plotly.offline as pyo
import plotly.graph_objs as go


app = dash.Dash()

np.random.seed(42)

random_x = np.random.randint(1,101,100)
random_y = np.random.randint(1,101,100)

app.layout = html.Div([dcc.Graph(id="scatterplot",
    #Figure on same format as plotly creation
    figure = {"data":[go.Scatter(
            x=random_x,
            y=random_y,
            mode="markers",
            marker= {
                    "size":6,
                    "color":"rgb(0,0,0)",
                    "line":{"width":0}
            }
            )],
            "layout": go.Layout(title="Scatterplot example") }
    ),
    #Simple copy to illustrate multiple plots
    dcc.Graph(id="scatterplot2",
        figure = {"data":[go.Scatter(
                x=random_x,
                y=random_y,
                mode="markers",
                marker= {
                        "size":6,
                        "color":"rgb(50,50,100)",
                        "symbol":"pentagon",
                        "line":{"width":0}
                }
                )],
                "layout": go.Layout(title="Scatterplot example 2") }
        )])

if __name__ == "__main__":
    app.run_server()
