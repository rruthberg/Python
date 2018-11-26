#DASH w callbacks
#Dashboarding on gapminder data with multiple inputs
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import numpy as np
import pandas as pd
import plotly.offline as pyo
import plotly.graph_objs as go
import base64

app = dash.Dash()

#Displaying jpeg from encoded file
def encode_image(image_file):
    encoded = base64.b64encode(open(image_file,"rb").read())
    return "data:image/png;base64,{}".format(encoded.decode())

#Read gapminder data
df = pd.read_csv("data/wheels.csv")

app.layout = html.Div([
    dcc.RadioItems(id="wheels",
        options = [{"label":i,"value":i} for i in df["wheels"].unique()],
        value=1
    ),
    html.Div(id="wheels_output"),
    html.Hr(),
    dcc.RadioItems(id="colors",
        options = [{"label":i,"value":i} for i in df["color"].unique()],
        value="blue"
    ),
    html.Div(id="colors_output"),
    html.Img(id="display_image", src="children",height=300),
    dcc.RangeSlider(id="range_slider",min=-10,max=10, marks={i:str(i) for i in range(-10,11)}, value=[-1,1]),
    html.H1(id="product"),

], style={"fontFamily":"helvetica", "fontSize":18})

@app.callback(Output("wheels_output","children"),
    [Input("wheels","value")]
)
def callback_a(wheels_value):
    return "You chose {}".format(wheels_value)

@app.callback(Output("colors_output","children"),
    [Input("colors","value")]
)
def callback_b(colors_value):
    return "You chose {}".format(colors_value)

@app.callback(Output("display_image","src"),
    [Input("wheels","value"), Input("colors","value")]
)
def callback_image(wheels_value,colors_value):
    path = "data/Images/"
    return encode_image(path+df[(df["wheels"]==wheels_value) & (df["color"]==colors_value)]["image"].values[0])

@app.callback(Output("product","children"),
    [Input("range_slider","value")]
)
def update_range_value(value_list):
    return value_list[0]*value_list[1]

if __name__ == "__main__":
    app.run_server()
