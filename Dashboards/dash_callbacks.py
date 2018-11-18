#DASH components intro
#Dashboarding with components
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
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
    dcc.Input(id="my-id",value="Initial text",type="text"), #NOT dependencies "Input"
    html.Div(id="my-div")
])


#Callback function
@app.callback(Output(component_id="my-div",component_property="children"),
    [Input(component_id="my-id",component_property="value")]
)
def update_output_div(input_value):
    return "You entered: {}".format(input_value)



if __name__ == "__main__":
    app.run_server()
