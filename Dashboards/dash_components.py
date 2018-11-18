#DASH components intro
#Dashboarding with components
import dash
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
import pandas as pd
import plotly.offline as pyo
import plotly.graph_objs as go


app = dash.Dash()

#Markdown text

mtext ="""
This is some text
I just want to say this.
"""


#Main html div = list of components, which can be nested and styled
app.layout = html.Div([
    dcc.Markdown(children=mtext),
    html.Label("Dropdown"),
    dcc.Dropdown(options=[
        {"label":"New York City","value":"NYC"},
        {"label":"San Francisco","value":"SF"},
        {"label":"Los Angeles","value":"LA"}
        ],
        value="SF"
    ),
    html.Label("Slider"),
    dcc.Slider(min=-10,max=10,step=0.5,value=0,
        marks={i: i for i in range(-10,10)}
    ),
    html.P(html.Label("Radio items")),
    dcc.RadioItems(options=[
        {"label":"New York City","value":"NYC"},
        {"label":"San Francisco","value":"SF"},
        {"label":"Los Angeles","value":"LA"}
        ],
        value="SF"
    )
])



if __name__ == "__main__":
    app.run_server()
