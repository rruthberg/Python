#Dashbard for Market data analysis with TA focus
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import numpy as np
import pandas as pd
import plotly.offline as pyo
import plotly.graph_objs as go
import plotly.figure_factory as ff

btcdat = pd.read_csv('data\\BTCUSD_1_20180101.csv',delimiter=',', encoding="utf-8")

def formatDate(str):
    return str[:10] + " " + str[11:15] + ":00"
#btcdat["Time"] = pd.to_datetime(btcdat["Time"].str[:10] + " " + btcdat["Time"].str[11:15] + ":00")
btcdat["Time"] = btcdat["Time"].apply(formatDate)
btcdat["Time"] = pd.to_datetime(btcdat["Time"])
#btcdat['Time'] = pd.to_datetime(btcdat.Time)
btcdat.sort_values(by=['Idx'], inplace=True, ascending=False)
print(btcdat.head())
print(btcdat.Time)

app = dash.Dash()


#Settings
colors = {"background":"#FFFFFF", "text":"#000000"} #store colors in same dict

#Texts
mtext ="""
Technical Analysis - BTC Data
"""
htext = "Market Analysis"


app.layout = html.Div([
    html.H1(htext,style={"textAlign":"left",
                            "color":colors["text"]})
    ,dcc.Markdown(children=mtext)
    ,html.Div(
        [
            html.Div([
                dcc.Graph(id="example1",
                    figure={"data":[
                        {"x":btcdat["Idx"],"y":btcdat["Close"],"type":"line","name":"BTCUSD"}
                    ],
                    "layout":{
                        "plot_bgcolor":colors["background"],
                        "paper_bgcolor":colors["background"],
                        "font":{"color":colors["text"]}
                        #,"title":"BTC Series"
                    }
                })
            ],style={'display': 'inline-block'})
            ,html.Div([
                dcc.Graph(id="scatterplot",
                    figure = {"data":[go.Scatter(
                            x=btcdat["RSI"],
                            y=btcdat["Volume"],
                            mode="markers",
                            marker= {
                                    "size":6,
                                    "color":"rgb(0,0,0)",
                                    "line":{"width":0}
                            }
                            )],
                            "layout": go.Layout(title="Scatterplot example") }
                    ),
            ],style={'display': 'inline-block'})
        ],
        style={'width': '100%', 'display': 'inline-block'}
    )
    ,html.Div(
        [
            html.Div([
                dcc.Graph(id="example2",
                    figure = {"data":[go.Histogram(x=btcdat["Close"].pct_change(),cumulative=dict(enabled=True))],
                            "layout": go.Layout(title="Daily Returns CDF") })
            ],style={'display': 'inline-block'})
            ,html.Div([
                dcc.Graph(id="histogram",
                    figure = {"data":[go.Histogram(x=btcdat["Close"].pct_change())],
                            "layout": go.Layout(title="Daily Returns Histogram") }
                    ),
            ],style={'display': 'inline-block'})
        ],
        style={'width': '100%', 'display': 'inline-block'}
    )
], style={"backgroundColor":colors["background"]})



if __name__ == "__main__":
    app.run_server()
