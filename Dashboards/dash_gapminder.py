#DASH w callbacks
#Dashboarding on gapminder data
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import numpy as np
import pandas as pd
import plotly.offline as pyo
import plotly.graph_objs as go


app = dash.Dash()

#Read gapminder data
df = pd.read_csv("data/gapminderDataFiveYear.csv")

#Markdown text

mtext ="""
This is some text
I just want to say this.
"""

#Get labels = unique values on year column
year_options = []
for year in df["year"].unique():
    year_options.append({"label":str(year),"value":year})

#Main html div = list of components, which can be nested and styled
app.layout = html.Div([
    dcc.Graph(id="graph"),
    dcc.Dropdown(id="year-picker",
        options = year_options, #auto-generated from def
        value = df["year"].min()
    )
    #,
    #dcc.Slider(
    #        id = "year-picker",
    #        min=df["year"].min(),
    #        max=df["year"].max(),
    #        step=5,
    #        value=df["year"].min(),
    #        marks=year_options["value"]
    #)
    #dcc.Input(id="my-id",value="Initial text",type="text"), #NOT dependencies "Input"
    #html.Div(id="my-div")
])


#Callback function for updating Figure
@app.callback(
    Output("graph","figure"),
    [Input("year-picker","value")]
)
def update_figure(selected_year):
    filtered_df = df[df["year"]==selected_year] #simple filter on year
    traces = []
    for continent_name in filtered_df["continent"].unique():
        df_by_continent = filtered_df[filtered_df["continent"]==continent_name]
        traces.append(go.Scatter(
            x=df_by_continent["gdpPercap"],
            y=df_by_continent["lifeExp"],
            mode="markers",
            opacity = 0.7,
            marker = {"size":15},
            name = continent_name
        ))
    return {"data": traces,
            "layout": go.Layout(title="GDP Per capita and Country",
                    xaxis = {"title":"GDP per cap", "type":"log"},
                    yaxis = {"title":"Life expectancy"}
                )
            }





if __name__ == "__main__":
    app.run_server()
