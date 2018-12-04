#Basic plotly examples/playground to visualize data
import numpy as np
import pandas as pd
import plotly.offline as pyo
import plotly.graph_objs as go
import plotly.figure_factory as ff
np.random.seed(42)


#Scatterplot
random_x = np.random.randint(1,101,100)
random_y = np.random.randint(1,101,100)
data = [go.Scatter(x=random_x,
                   y=random_y,
                   mode="markers",
                   marker = dict(
                       size=12,
                       color="rgb(0,0,40)",
                       symbol="circle",
                       line = {"width":1}
                   )
                  )]
layout = go.Layout(title="Random nums",
                xaxis=dict(title='NumX'),
                yaxis=dict(title='NumY'),
                  hovermode="closest")
fig = go.Figure(data=data, layout=layout)
pyo.plot(fig,filename='plot_out/scatterExample.html')

#Line charts
x_values = np.linspace(0,1,100)
y_values = np.random.randn(100) #normal dist

trace0 = go.Scatter(x=x_values, y=y_values+5,
                  mode = "markers", name = "markers")
trace1 = go.Scatter(x=x_values, y=y_values,
                  mode = "lines", name = "mylines")
trace2 = go.Scatter(x=x_values, y=y_values-5,
                  mode = "lines+markers", name = "best one")
data = [trace0,trace1,trace2]
layout = go.Layout(title="Line chart")
fig = go.Figure(data=data, layout=layout)
pyo.plot(fig,filename='plot_out/lineExample.html')

#Nicer example using real data
df = pd.read_csv("data/nst-est2017-alldata.csv")
df2 = df[df["DIVISION"] == "1"] #filter on state NE
df2.set_index("NAME",inplace=True)
list_pop_col = [col for col in df2.columns if col.startswith("POP")] #list comprehension to only select colnames starting with "POP" -> only population cols
df2 = df2[list_pop_col]
data = [go.Scatter(x=df2.columns,
               y=df2.loc[name],
               mode="lines",
               name=name) for name in df2.index]
pyo.plot(data,filename='plot_out/line2Example.html')

#Bar charts
df = pd.read_csv("data/2018WinterOlympics.csv")
trace1 = go.Bar(x=df["NOC"],
                y=df["Gold"],
                name="Gold",
                marker={"color":"#FFD700"})
trace2 = go.Bar(x=df["NOC"],
                y=df["Silver"],
                name="Silver",
                marker={"color":"#9EA0A1"})
trace3 = go.Bar(x=df["NOC"],
                y=df["Bronze"],
                name="Bronze",
                marker={"color":"#CD7F32"})

#data = [go.Bar(x=df["NOC"], y=df["Total"])]
data = [trace1, trace2, trace3]
layout = go.Layout(title="Medals",barmode="stack") #stack gives stacked chart, none = nested
fig = go.Figure(data=data,layout=layout)
pyo.plot(fig,filename='plot_out/barExample.html')


#Bubble plots
df = pd.read_csv("data/mpg.csv")
data = [go.Scatter(x=df["horsepower"],
                  y=df["mpg"],
                  text=df["name"],
                  mode="markers",
                  marker=dict(size=df["weight"]/100, color=df["cylinders"],showscale=True))]
layout = go.Layout(title="Bubble chart")
fig = go.Figure(data=data,layout=layout)
pyo.plot(fig,filename='plot_out/bubbleExample.html')


#Box plots
y = [1,14,14,15,16,18,18,19,19,20,20,23,24,26,27,27,28,29,33,54]
snodgrass = [.209,.205,.196,.210,.202,.207,.224,.223,.220,.201]
twain = [.225,.262,.217,.240,.230,.229,.235,.217]
#data = [go.Box(y=y,boxpoints="all",jitter=0.3,pointpos=0)]
#data = [go.Box(y=y,boxpoints="outliers")]
data = [go.Box(y=snodgrass,name="Snoddgrass"),
       go.Box(y=twain,name="Twain")]
pyo.plot(data,filename='plot_out/boxExample.html')

#Distribution plots
x1 = np.random.randn(200)-2
x2 = np.random.randn(200)
x3 = np.random.randn(200)+2
x4 = np.random.randn(200)+4
hist_data = [x1,x2,x3,x4]
group_labels = ["X1","X2","X3","X4"]

fig = ff.create_distplot(hist_data,group_labels,bin_size=[.2,.2,.2,.2])
pyo.plot(fig,filename='plot_out/distExample.html')

#Heatmaps
df = pd.read_csv("data/2010SantaBarbaraCA.csv")
data = [go.Heatmap(x=df["DAY"],
                  y=df["LST_TIME"],
                  z=df["T_HR_AVG"].values.tolist(),
                   colorscale="Jet")] # z needs to be on list
layout = go.Layout(title="SB CA Temp")
fig = go.Figure(data=data,layout=layout)
pyo.plot(fig,filename='plot_out/heatmapExample.html')

#Multiple heatmaps with subplots
df1 = pd.read_csv("data/2010SitkaAK.csv")
df2 = pd.read_csv("data/2010SantaBarbaraCA.csv")
df3 = pd.read_csv("data/2010YumaAZ.csv")
trace1 = go.Heatmap(x=df1["DAY"],
                  y=df1["LST_TIME"],
                  z=df1["T_HR_AVG"].values.tolist(),
                   colorscale="Jet",
                   zmin=5,
                   zmax=40)
trace2 = go.Heatmap(x=df2["DAY"],
                  y=df2["LST_TIME"],
                  z=df2["T_HR_AVG"].values.tolist(),
                   colorscale="Jet",
                   zmin=5,
                   zmax=40)
trace3 = go.Heatmap(x=df3["DAY"],
                  y=df3["LST_TIME"],
                  z=df3["T_HR_AVG"].values.tolist(),
                   colorscale="Jet",
                   zmin=5,
                   zmax=40)

fig = tools.make_subplots(rows=1,cols=3,subplot_titles=["Sitka","SB","Yuma"],
                         shared_yaxes=False)
#Put traces in correct section:
fig.append_trace(trace1,1,1)
fig.append_trace(trace2,1,2)
fig.append_trace(trace3,1,3)
fig["layout"].update(title="Temps for 3 cities")
pyo.plot(fig,filename='plot_out/multiheatmapExample.html')
